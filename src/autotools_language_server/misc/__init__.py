r"""Misc
========
"""

from typing import Any


def get_schema(filetype: str) -> dict[str, Any]:
    r"""Get schema.

    :param filetype:
    :type filetype: str
    :rtype: dict[str, Any]
    """
    if filetype == "config":
        from .autoconf import init_schema
    elif filetype == "make":
        from .make import init_schema
    else:
        raise NotImplementedError(filetype)
    return init_schema()[filetype]
