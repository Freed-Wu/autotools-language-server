r"""Test utils"""

import os

from lsp_tree_sitter.diagnose import check
from make_language_server.finders import DIAGNOSTICS_FINDER_CLASSES
from make_language_server.utils import get_schema, parser

PATH = os.path.dirname(__file__)


class Test:
    r"""Test."""

    @staticmethod
    def test_check() -> None:
        r"""Test check.

        :rtype: None
        """
        result = check(
            [os.path.join(PATH, "Makefile")],
            parser.parse,
            DIAGNOSTICS_FINDER_CLASSES,
            None,
        )
        assert result > 0

    @staticmethod
    def test_get_schema() -> None:
        r"""Test get schema.

        :rtype: None
        """
        assert get_schema()["properties"].get("CURDIR")
