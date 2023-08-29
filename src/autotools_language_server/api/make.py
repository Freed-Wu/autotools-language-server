r"""Api Make
============
"""
import os
from glob import glob
from gzip import decompress

from platformdirs import site_data_dir


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


def get_content(filename) -> str:
    r"""Get content.

    :param filename:
    :rtype: str
    """
    filename = glob(os.path.join(site_data_dir("info"), filename + "*"))[0]
    with open(filename, "rb") as f:
        content = f.read()
        if filename.endswith(".gz"):
            content = decompress(content)
        content = content.decode()
    return content


def init_make_document() -> dict[str, str]:
    r"""Init make document.

    :rtype: dict[str, str]
    """
    macros = {}

    _lines = get_content("make.info-2").splitlines()
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
    return macros
