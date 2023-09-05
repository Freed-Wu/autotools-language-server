r"""Test server"""
import os

from autotools_language_server._tree_sitter import get_parser
from autotools_language_server.diagnostics import diagnostic

PATH = os.path.dirname(__file__)


class Test:
    r"""Test."""

    @staticmethod
    def test_diagnostic() -> None:
        r"""Test diagnostic.

        :rtype: None
        """
        parser = get_parser()
        with open(os.path.join(PATH, "Makefile")) as f:
            text = f.read()
        tree = parser.parse(bytes(text, "utf-8"))
        assert len(diagnostic(tree, ""))
