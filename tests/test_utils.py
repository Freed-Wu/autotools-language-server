r"""Test utils"""
import os

from autotools_language_server.parser import parse
from autotools_language_server.tree_sitter_lsp.diagnose import check
from autotools_language_server.utils import DIAGNOSTICS_FINDERS

PATH = os.path.dirname(__file__)


class Test:
    r"""Test."""

    @staticmethod
    def test_check() -> None:
        r"""Test check.

        :rtype: None
        """
        result = check(
            [os.path.join(PATH, "Makefile")], DIAGNOSTICS_FINDERS, parse
        )
        assert result > 0
