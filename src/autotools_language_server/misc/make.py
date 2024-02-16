r"""Make
========
"""

from typing import Any

from tree_sitter_lsp.misc import get_info

from .._metainfo import SOURCE, project


def get_macro(line: str, begin: str = "$(", end: str = ")") -> str:
    r"""Get macro.

    :param line:
    :type line: str
    :param begin:
    :type begin: str
    :param end:
    :type end: str
    :rtype: str
    """
    return line.strip("'").lstrip(begin).rstrip(end).split()[0]


def match(line: str, begin: str = "'", end: str = "'") -> bool:
    r"""Match.

    :param line:
    :type line: str
    :param begin:
    :type begin: str
    :param end:
    :type end: str
    :rtype: bool
    """
    macro = line.strip("'")
    return (
        line.startswith(begin)
        and line.endswith(end)
        and (not macro.startswith("-") or macro == "-include")
        and (macro not in ["0", "1", "2"])
    )


def reset(
    macros: dict[str, str], _macros: list[str], lines: list[str]
) -> tuple[dict[str, str], list[str], list[str]]:
    r"""Reset.

    :param macros:
    :type macros: dict[str, str]
    :param _macros:
    :type _macros: list[str]
    :param lines:
    :type lines: list[str]
    :rtype: tuple[dict[str, str], list[str], list[str]]
    """
    for macro in _macros:
        macros[macro] = "\n".join(line for line in lines if line)
    _macros = []
    lines = []
    return macros, _macros, lines


def init_schema() -> dict[str, dict[str, Any]]:
    r"""Init schema.

    :rtype: dict[str, dict[str, Any]]
    """
    filetype = "make"
    schema = {
        "$id": (
            f"{SOURCE}/blob/main/"
            f"src/termux_language_server/assets/json/{filetype}.json"
        ),
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$comment": (
            "Don't edit this file directly! It is generated by "
            f"`{project} --generate-schema={filetype}`."
        ),
        "type": "object",
        "properties": {},
    }
    macros = {}

    _lines = get_info("make.info-2").splitlines()
    _macros = []
    lines = []
    lastline = ""
    for line in _lines:
        if match(line) and not match(lastline):
            macros, _macros, lines = reset(macros, _macros, lines)
            _macros += [get_macro(line)]
            lines += [line]
        elif match(line) and match(lastline):
            _macros += [get_macro(line)]
            lines += [line]
        elif _macros and (line.startswith("     ") or line == ""):
            lines += [line]
        else:
            macros, _macros, lines = reset(macros, _macros, lines)
        lastline = line
    for k, v in macros.items():
        codes = []
        docs = []
        for line in v.splitlines():
            if line.startswith("'") and line.endswith("'"):
                codes += [line.strip("'")]
            else:
                docs += [line.strip()]
        code = "\n".join(codes)
        doc = " ".join(docs)
        if code == k:
            schema["properties"][k] = {"description": doc}
        else:
            schema["properties"][k] = {
                "description": f"""```make
{code}
```
{doc}"""
            }
    return {filetype: schema}
