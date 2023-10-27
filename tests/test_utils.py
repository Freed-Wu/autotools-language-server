r"""Test utils"""
import os

from tree_sitter_languages import get_parser
from tree_sitter_lsp.diagnose import check

from autotools_language_server.finders import DIAGNOSTICS_FINDER_CLASSES
from autotools_language_server.utils import get_filetype, get_schema

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
            get_parser("make").parse,
            DIAGNOSTICS_FINDER_CLASSES,
            get_filetype,
        )
        assert result > 0

    @staticmethod
    def test_get_schema() -> None:
        r"""Test get schema.

        :rtype: None
        """
        assert get_schema("config")["properties"].get("AC_INIT")
        assert get_schema("make")["properties"].get("CURDIR")
