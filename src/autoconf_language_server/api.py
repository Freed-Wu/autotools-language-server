r"""Api
=======
"""
import json
import os
from gzip import decompress
from typing import Literal

from platformdirs import site_data_dir, user_cache_dir

START = " -- Macro: "


def get_macro(line: str) -> str:
    r"""Get macro.

    :param line:
    :type line: str
    :rtype: str
    """
    return line.lstrip(START).split(" ")[0]


def reset(
    macros: dict[str, str], macro: str, macro2: str, lines: list[str]
) -> tuple[dict[str, str], str, str, list[str]]:
    r"""Reset.

    :param macros:
    :type macros: dict[str, str]
    :param macro: 1st macro
    :type macro: str
    :param macro2: 2nd macro, maybe doesn't exist
    :type macro2: str
    :param lines:
    :type lines: list[str]
    :rtype: tuple[dict[str, str], str, str, list[str]]
    """
    if macro:
        macros[macro] = "\n".join(lines)
        if macro2:
            macros[macro2] = macros[macro]
            macro2 = ""
        macro = ""
        lines = []
    return macros, macro, macro2, lines


def init_document() -> dict[str, str]:
    r"""Init document.

    :rtype: dict[str, str]
    """
    with open(
        os.path.join(site_data_dir("info"), "autoconf.info.gz"), "rb"
    ) as f:
        _lines = decompress(f.read()).decode().splitlines()
    macros = {}
    macro = ""
    macro2 = ""
    lines = []
    lastline = ""
    for line in _lines:
        # -- Macro: AC_INIT (PACKAGE, VERSION, [BUG-REPORT], [TARNAME], [URL])
        #     ...
        if line.startswith(START) and not lastline.startswith(START):
            macros, macro, macro2, lines = reset(macros, macro, macro2, lines)
            macro = get_macro(line)
            lines += [line]
        # -- Macro: AC_CONFIG_MACRO_DIRS (DIR1 [DIR2 ... DIRN])
        # -- Macro: AC_CONFIG_MACRO_DIR (DIR)
        #     ...
        elif line.startswith(START) and lastline.startswith(START):
            macro2 = get_macro(line)
            lines += [line]
        # ...
        #
        # ...
        # or not
        #    text indented 3 spaces is not document
        elif macro and (len(line) < 4 or line[4] == " "):
            lines += [line]
        #    text indented 3 spaces is not document
        elif len(line) > 4 and line[4] != " ":
            macros, macro, macro2, lines = reset(macros, macro, macro2, lines)
        lastline = line
    return macros


def get_document(
    method: Literal["builtin", "cache", "system"] = "builtin"
) -> dict[str, str]:
    r"""Get document. ``builtin`` will use builtin autoconf.json. ``cache``
    will generate a cache from ``${XDG_CACHE_DIRS:-/usr/share}
    /info/autoconf.info.gz``. ``system`` is same as ``cache`` except it doesn't
    generate cache. Some distribution's autoconf doesn't contain textinfo. So
    we use ``builtin`` as default.

    :param method:
    :type method: Literal["builtin", "cache", "system"]
    :rtype: dict[str, str]
    """
    if method == "builtin":
        file = os.path.join(
            os.path.join(
                os.path.join(os.path.dirname(__file__), "assets"), "json"
            ),
            "autoconf.json",
        )
        with open(file, "r") as f:
            document = json.load(f)
    elif method == "cache":
        if not os.path.exists(user_cache_dir("autoconf.json")):
            document = init_document()
            with open(user_cache_dir("autoconf.json"), "w") as f:
                json.dump(document, f)
        else:
            with open(user_cache_dir("autoconf.json"), "r") as f:
                document = json.load(f)
    else:
        document = init_document()
    return document
