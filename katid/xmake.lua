-- luacheck: ignore 111 113 143
---@diagnostic disable: undefined-global, undefined-field
includes("packages/k/kati")
add_rules("mode.debug", "mode.release")

add_requires("lsp-framework")
-- add a static library
add_requires("kati", { system = false })
set_languages("c++20")

target("katid")
do
    set_kind("binary")
    add_defines("NOLOG")
    add_files("src/*.cc")
    add_installfiles("assets/Makefile", { prefixdir = "share/katid" })
    add_packages("lsp-framework")
    if not is_mode("debug") then
        add_packages("kati")
    else
        add_includedirs("kati/src")
        add_deps("kati")
        on_load(
            function(target)
                if not os.isdir("kati") then
                    import("devel.git")
                    git.clone("https://github.com/google/kati", { depth = 1 })
                end
            end
        )
    end
end

target("kati")
do
    set_kind("static")
    add_defines("NOLOG")
    add_includedirs("kati/src")
    set_optimize("fast")
    add_installfiles("kati/src/*.h", { prefixdir = "include" })
    add_files(
        "kati/src/affinity.cc",
        "kati/src/command.cc",
        "kati/src/dep.cc",
        "kati/src/eval.cc",
        "kati/src/exec.cc",
        "kati/src/expr.cc",
        "kati/src/file.cc",
        "kati/src/file_cache.cc",
        "kati/src/fileutil.cc",
        "kati/src/find.cc",
        "kati/src/flags.cc",
        "kati/src/func.cc",
        "kati/src/io.cc",
        "kati/src/log.cc",
        "kati/src/ninja.cc",
        "kati/src/parser.cc",
        "kati/src/regen.cc",
        "kati/src/regen_dump.cc",
        "kati/src/rule.cc",
        "kati/src/stats.cc",
        "kati/src/stmt.cc",
        "kati/src/stringprintf.cc",
        "kati/src/strutil.cc",
        "kati/src/symtab.cc",
        "kati/src/timeutil.cc",
        "kati/src/var.cc",
        "kati/src/version_unknown.cc"
    )
end
