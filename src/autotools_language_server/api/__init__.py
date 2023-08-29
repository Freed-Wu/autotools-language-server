r"""Api
=======
"""
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
