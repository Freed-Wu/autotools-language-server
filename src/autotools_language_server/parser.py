r"""Parser
==========
"""
import os
from glob import glob

from tree_sitter import Language, Parser, Tree

LIB = glob(
    os.path.join(
        os.path.join(os.path.join(os.path.dirname(__file__), "data"), "lib"),
        "*",
    )
)[0]
PARSER = Parser()
PARSER.set_language(Language(LIB, "make"))


def parse(source: bytes) -> Tree:
    r"""Parse.

    :param source:
    :type source: bytes
    :rtype: Tree
    """
    return PARSER.parse(source)
