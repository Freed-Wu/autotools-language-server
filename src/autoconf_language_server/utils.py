r"""Utils
=========
"""

import json
import os
from typing import Any

from . import FILETYPE

SCHEMAS = {}


def get_schema(filetype: FILETYPE = "config") -> dict[str, Any]:
    r"""Get schema.

    :param filetype:
    :type filetype: FILETYPE
    :rtype: dict[str, Any]
    """
    if filetype not in SCHEMAS:
        file = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "json",
            f"{filetype}.json",
        )
        with open(file) as f:
            SCHEMAS[filetype] = json.load(f)
    return SCHEMAS[filetype]
