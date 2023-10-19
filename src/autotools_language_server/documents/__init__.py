r"""Documents
=============
"""
import json
import os
from typing import Literal

from platformdirs import user_cache_dir

from .autoconf import init_autoconf_document
from .make import init_make_document


def init_document() -> dict[str, tuple[str, str]]:
    r"""Init document.

    :rtype: dict[str, tuple[str, str]]
    """
    result = {}
    for k, v in init_autoconf_document().items():
        result[k] = (v, "config")
    for k, v in init_make_document().items():
        result[k] = (v, "make")
    return result


def get_document(
    method: Literal["builtin", "cache", "system"] = "builtin"
) -> dict[str, tuple[str, str]]:
    r"""Get document. ``builtin`` will use builtin autotools.json. ``cache``
    will generate a cache from
    ``${XDG_CACHE_DIRS:-/usr/share}/info/autoconf.info.gz``,
    ``${XDG_CACHE_DIRS:-/usr/share}/info/automake.info-1.gz``,
    ``${XDG_CACHE_DIRS:-/usr/share}/info/make.info-2.gz``.
    ``system`` is same as ``cache`` except it doesn't generate cache. Some
    distribution's autotools doesn't contain textinfo. So we use ``builtin`` as
    default.

    :param method:
    :type method: Literal["builtin", "cache", "system"]
    :rtype: dict[str, tuple[str, str]]
    """
    if method == "builtin":
        file = os.path.join(
            os.path.join(
                os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "assets"
                ),
                "json",
            ),
            "autotools.json",
        )
        with open(file, "r") as f:
            document = json.load(f)
    elif method == "cache":
        from . import init_document

        if not os.path.exists(user_cache_dir("autotools.json")):
            document = init_document()
            with open(user_cache_dir("autotools.json"), "w") as f:
                json.dump(document, f)
        else:
            with open(user_cache_dir("autotools.json"), "r") as f:
                document = json.load(f)
    else:
        from . import init_document

        document = init_document()
    return document


def get_filetype(uri: str) -> Literal["config", "make", ""]:
    r"""Get filetype.

    :param uri:
    :type uri: str
    :rtype: Literal["config", "make", ""]
    """
    if (
        uri.split(os.path.extsep)[-1] in ["mk"]
        or os.path.basename(uri).split(os.path.extsep)[0] == "Makefile"
    ):
        return "make"
    if os.path.basename(uri) == "configure.ac":
        return "config"
    return ""
