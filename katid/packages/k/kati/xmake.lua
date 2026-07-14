-- luacheck: ignore 111 113 143
---@diagnostic disable: undefined-global, undefined-field
package("kati")
do
    set_homepage("https://github.com/google/kati")
    set_description("An experimental GNU make clone")

    set_urls("https://github.com/google/kati.git")

    on_install(function(package)
        io.writefile("xmake.lua", [[
add_rules("mode.debug", "mode.release")
set_languages("c++20")

target("ckati")
do
    set_kind("binary")
    add_defines("NOLOG")
    add_deps("kati")
    add_files("src/main.cc")
end

target("kati")
do
    if is_mode("debug") then
        set_optimize("fast")
    end
    set_kind("static")
    add_defines("NOLOG")
    add_installfiles("src/*.h", { prefixdir = "include" })
    add_files(
        "src/affinity.cc",
        "src/command.cc",
        "src/dep.cc",
        "src/eval.cc",
        "src/exec.cc",
        "src/expr.cc",
        "src/file.cc",
        "src/file_cache.cc",
        "src/fileutil.cc",
        "src/find.cc",
        "src/flags.cc",
        "src/func.cc",
        "src/io.cc",
        "src/log.cc",
        "src/ninja.cc",
        "src/parser.cc",
        "src/regen.cc",
        "src/regen_dump.cc",
        "src/rule.cc",
        "src/stats.cc",
        "src/stmt.cc",
        "src/stringprintf.cc",
        "src/strutil.cc",
        "src/symtab.cc",
        "src/timeutil.cc",
        "src/var.cc",
        "src/version_unknown.cc"
    )
end
        ]])
        import("package.tools.xmake").install(package)
    end)

    on_test(function(package)
        if not package:is_cross() then
            for _, tool in ipairs({ "ckati" }) do
                if package:config(tool) then
                    os.vrunv(tool, { "--realpath", "." })
                end
            end
        end
    end)
end
package_end()
