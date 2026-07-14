// Copyright 2015 Google Inc. All rights reserved
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// +build ignore

#include <limits.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <filesystem>
#include <string_view>

#include "eval.h"
#include "exec.h"
#include "file.h"
#include "file_cache.h"
#include "log.h"
#include "ninja.h"
#include "parser.h"
#include "stmt.h"
#include "stringprintf.h"
#include "symtab.h"
#include "timeutil.h"
#include "var.h"

// We know that there are leaks in Kati. Turn off LeakSanitizer by default.
extern "C" const char *__asan_default_options() {
  return "detect_leaks=0:allow_user_segv_handler=1";
}

static void SetVar(std::string_view l, VarOrigin origin, Frame *definition,
                   Loc loc) {
  size_t found = l.find('=');
  CHECK(found != std::string::npos);
  Symbol lhs = Intern(l.substr(0, found));
  std::string_view rhs = l.substr(found + 1);
  lhs.SetGlobalVar(new RecursiveVar(Value::NewLiteral(rhs.data()), origin,
                                    definition, loc, rhs.data()));
}

extern "C" char **environ;

class SegfaultHandler {
public:
  explicit SegfaultHandler(Evaluator *ev);
  ~SegfaultHandler();

  void handle(int, siginfo_t *, void *);

private:
  static SegfaultHandler *global_handler;

  void dumpstr(const char *s) const {
    (void)write(STDERR_FILENO, s, strlen(s));
  }
  void dumpint(int i) const {
    char buf[11];
    char *ptr = buf + sizeof(buf) - 1;

    if (i < 0) {
      i = -i;
      dumpstr("-");
    } else if (i == 0) {
      dumpstr("0");
      return;
    }

    *ptr = '\0';
    while (ptr > buf && i > 0) {
      *--ptr = '0' + (i % 10);
      i = i / 10;
    }

    dumpstr(ptr);
  }

  Evaluator *ev_;

  struct sigaction orig_action_;
  struct sigaction new_action_;
};

SegfaultHandler *SegfaultHandler::global_handler = nullptr;

SegfaultHandler::SegfaultHandler(Evaluator *ev) : ev_(ev) {
  CHECK(global_handler == nullptr);
  global_handler = this;

  // Construct an alternate stack, so that we can handle stack overflows.
  stack_t ss;
  ss.ss_sp = malloc(SIGSTKSZ * 2);
  CHECK(ss.ss_sp != nullptr);
  ss.ss_size = SIGSTKSZ * 2;
  ss.ss_flags = 0;
  if (sigaltstack(&ss, nullptr) == -1) {
    PERROR("sigaltstack");
  }

  // Register our segfault handler using the alternate stack, falling
  // back to the default handler.
  sigemptyset(&new_action_.sa_mask);
  new_action_.sa_flags = SA_ONSTACK | SA_SIGINFO | SA_RESETHAND;
  new_action_.sa_sigaction = [](int sig, siginfo_t *info, void *context) {
    if (global_handler != nullptr) {
      global_handler->handle(sig, info, context);
    }

    raise(SIGSEGV);
  };
  sigaction(SIGSEGV, &new_action_, &orig_action_);
}

void SegfaultHandler::handle(int sig, siginfo_t *info, void *context) {
  // Avoid fprintf in case it allocates or tries to do anything else that may
  // hang.
  dumpstr("*kati*: Segmentation fault, last evaluated line was ");
  dumpstr(ev_->loc().filename);
  dumpstr(":");
  dumpint(ev_->loc().lineno);
  dumpstr("\n");

  // Run the original handler, in case we've been preloaded with libSegFault
  // or similar.
  if (orig_action_.sa_sigaction != nullptr) {
    orig_action_.sa_sigaction(sig, info, context);
  }
}

SegfaultHandler::~SegfaultHandler() {
  sigaction(SIGSEGV, &orig_action_, nullptr);
  global_handler = nullptr;
}

int Run(std::string makefile) {
  if (makefile == "") {
#ifdef NDEBUG
    try {
      makefile = std::filesystem::canonical("/proc/self/exe");
    } catch (const std::filesystem::filesystem_error &e) {
      return 1;
    }
    makefile = Dirname(Dirname(makefile));
    std::vector<const char *> args = {"share", "katid", "Makefile"};
#else
    makefile = Dirname(Dirname(__FILE__));
    std::vector<const char *> args = {"assets", "Makefile"};
#endif
    args.emplace(args.begin(), makefile.c_str());
    makefile = JoinStrings(args, "/");
  }

  Evaluator ev;
  if (!ev.Start()) {
    return 1;
  }
  Intern("MAKEFILE_LIST")
      .SetGlobalVar(new SimpleVar(StringPrintf(" %s", makefile.c_str()),
                                  VarOrigin::FILE, ev.CurrentFrame(),
                                  ev.loc()));
  for (char **p = environ; *p; p++) {
    SetVar(*p, VarOrigin::ENVIRONMENT, nullptr, Loc());
  }
  SegfaultHandler segfault(&ev);

  ev.in_toplevel_makefile();

  {
    ScopedFrame eval_frame(ev.Enter(FrameType::PHASE, "*parse*", Loc()));
    ScopedTimeReporter tr("eval time");

    ScopedFrame file_frame(ev.Enter(FrameType::PARSE, makefile, Loc()));
    const Makefile &mk = MakefileCacheManager::Get().ReadMakefile(makefile);
    for (Stmt *stmt : mk.stmts()) {
      LOG("%s", stmt->DebugString().c_str());
      stmt->Eval(&ev);
    }
  }

  for (ParseErrorStmt *err : GetParseErrors()) {
    WARN_LOC(err->loc(), "warning for parse error in an unevaluated line: %s",
             err->msg.c_str());
  }

  ev.Finish();
  return 0;
}
