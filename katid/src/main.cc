#include <lsp/connection.h>
#include <lsp/io/standardio.h>
#include <lsp/messagehandler.h>
#include <lsp/messages.h>

#include "run.h"

int main(int argc, char *argv[]) {
  auto connection = lsp::Connection(lsp::io::standardIO());
  auto messageHandler = lsp::MessageHandler(connection);
#ifndef NDEBUG
  Run("");
#endif

  messageHandler
      .add<lsp::requests::Initialize>(
          [](lsp::requests::Initialize::Params &&params) {
            Run("");
            return lsp::requests::Initialize::Result{
                .capabilities =
                    {
                        .completionProvider = lsp::CompletionOptions{},
                        .hoverProvider = true,
                        .documentLinkProvider = lsp::DocumentLinkOptions{},
                    },
                .serverInfo =
                    lsp::InitializeResultServerInfo{
                        .name = "katid",
                        .version = "0.0.1",
                    },
            };
          })
      .add<lsp::requests::TextDocument_Completion>(
          [](lsp::requests::TextDocument_Completion::Params &&params) {
            return lsp::TextDocument_CompletionResult{lsp::CompletionList{
                .isIncomplete = false,
                .items =
                    {
                        {
                            .label = "foo",
                            .kind = lsp::CompletionItemKind::Variable,
                        },
                        {
                            .label = "foz",
                            .kind = lsp::CompletionItemKind::Variable,
                        },
                    },
            }};
          })
      .add<lsp::requests::TextDocument_Hover>(
          [](lsp::requests::TextDocument_Hover::Params &&params) {
            return lsp::TextDocument_HoverResult{
                lsp::Hover{.contents = lsp::MarkupContent{
                               .kind = lsp::MarkupKind::Markdown,
                               .value = "hello",
                           }}};
          })
      .add<lsp::requests::TextDocument_DocumentLink>(
          [](lsp::requests::TextDocument_DocumentLink::Params &&params) {
            return lsp::TextDocument_DocumentLinkResult{{lsp::DocumentLink{
                .range =
                    lsp::Range{
                        .start =
                            {
                                .line = 1,
                                .character = 1,
                            },
                        .end =
                            {
                                .line = 2,
                                .character = 2,
                            },
                    },
                .target = lsp::Uri::parse("/home/wzy/README.md"),
            }}};
          });

  while (true)
    messageHandler.processIncomingMessages();
  return EXIT_SUCCESS;
}
