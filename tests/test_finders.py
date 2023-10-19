r"""Test finders."""
import os

from autotools_language_server.finders import DefinitionFinder
from autotools_language_server.parser import parse
from autotools_language_server.tree_sitter_lsp import UNI

PATH = os.path.dirname(__file__)


class Test:
    r"""Test."""

    @staticmethod
    def test_DefinitionFinder() -> None:
        file = os.path.join(PATH, "Makefile")
        with open(file, "rb") as f:
            text = f.read()
        tree = parse(text)
        finder = DefinitionFinder(
            tree.root_node.children[10]
            .children[1]
            .children[0]
            .children[0]
            .children[2]
        )
        result = finder(UNI(file, tree.root_node.children[9].children[0]))
        assert result is True
