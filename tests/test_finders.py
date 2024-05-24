r"""Test finders."""

import os

from lsp_tree_sitter import UNI
from make_language_server.finders import DefinitionFinder
from make_language_server.utils import parser

PATH = os.path.dirname(__file__)


class Test:
    r"""Test."""

    @staticmethod
    def test_DefinitionFinder() -> None:
        file = os.path.join(PATH, "Makefile")
        with open(file, "rb") as f:
            text = f.read()
        tree = parser.parse(text)
        finder = DefinitionFinder(
            tree.root_node.children[13]
            .children[1]
            .children[0]
            .children[0]
            .children[2]
        )
        result = finder(UNI(file, tree.root_node.children[12].children[0]))
        assert result is True
