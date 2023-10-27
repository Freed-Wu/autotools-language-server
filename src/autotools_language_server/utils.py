r"""Utils
=========
"""
import json
import os
from typing import Any, Literal

from . import FILETYPE

SCHEMAS = {}


def get_schema(filetype: FILETYPE) -> dict[str, Any]:
    r"""Get schema.

    :param filetype:
    :type filetype: FILETYPE
    :rtype: dict[str, Any]
    """
    if filetype not in SCHEMAS:
        file = os.path.join(
            os.path.join(
                os.path.join(os.path.dirname(__file__), "assets"),
                "json",
            ),
            f"{filetype}.json",
        )
        with open(file, "r") as f:
            SCHEMAS[filetype] = json.load(f)
    return SCHEMAS[filetype]


def get_filetype(uri: str) -> FILETYPE | Literal[""]:
    r"""Get filetype.

    :param uri:
    :type uri: str
    :rtype: FILETYPE | Literal[""]
    """
    basename = os.path.basename(uri)
    ext = uri.split(os.path.extsep)[-1]
    if basename == "configure.ac":
        return "config"
    if ext == "mk" or basename.split(os.path.extsep)[0] == "Makefile":
        return "make"
    return ""
