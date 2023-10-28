r"""Finders
===========
"""
import os
from dataclasses import dataclass

from lsprotocol.types import DiagnosticSeverity
from tree_sitter import Node, Tree
from tree_sitter_languages import get_parser
from tree_sitter_lsp import UNI, Finder
from tree_sitter_lsp.finders import ErrorFinder, MissingFinder, RepeatedFinder


@dataclass
class InvalidPathFinder(Finder):
    r"""Invalidpathfinder."""

    message: str = "{{uni.get_text()}}: no such file"
    severity: DiagnosticSeverity = DiagnosticSeverity.Error

    @staticmethod
    def get_option(uni: UNI) -> str:
        r"""Get option.

        :param uni:
        :type uni: UNI
        :rtype: str
        """
        option = ""
        if parent := uni.node.parent:
            if children := getattr(parent.parent, "children", None):
                if len(children) > 0:
                    option = children[0].type
        return option

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        path = self.uni2path(uni)
        option = self.get_option(uni)
        if parent := uni.node.parent:
            return (
                uni.node.type == "word"
                and parent.type == "list"
                and option == "include"
                and not os.path.isfile(path)
            )
        return False


@dataclass
class RepeatedTargetFinder(RepeatedFinder):
    r"""Repeatedtargetfinder."""

    message: str = "{{uni.get_text()}}: is repeated on {{_uni}}"
    severity: DiagnosticSeverity = DiagnosticSeverity.Warning

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """
        self.parser = get_parser("make")

    def is_include_node(self, node: Node) -> bool:
        r"""Is include node.

        :param node:
        :type node: Node
        :rtype: bool
        """
        if parent := node.parent:
            return node.type == "word" and parent.type == "list"
        return False

    def parse(self, code: bytes) -> Tree:
        r"""Parse.

        :param code:
        :type code: bytes
        :rtype: Tree
        """
        return self.parser.parse(code)

    def filter(self, uni: UNI) -> bool:
        r"""Filter.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        if parent := uni.node.parent:
            text = uni.get_text()
            return (
                uni.node.type == "word"
                and parent.type == "targets"
                and not (text.startswith(".") and text.isupper())
            )
        return False


# https://github.com/alemuller/tree-sitter-make/issues/22
@dataclass(init=False)
class DefinitionFinder(RepeatedTargetFinder):
    r"""Definitionfinder."""

    def __init__(self, node: Node) -> None:
        r"""Init.

        :param node:
        :type node: Node
        :rtype: None
        """
        super().__init__()
        self.name = UNI.node2text(node)
        parent = node.parent
        if parent is None:
            raise TypeError
        if parent.type == "arguments":
            self.is_define = self.is_function_define
            # https://github.com/alemuller/tree-sitter-make/issues/8
            self.name = UNI.node2text(node).split(",")[0]
        elif parent.type == "variable_reference":
            self.is_define = self.is_variable_define
        elif parent.type == "prerequisites":
            self.is_define = self.is_target_define
        else:
            raise NotImplementedError

    def is_function_define(self, uni: UNI) -> bool:
        r"""Is function define.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        parent = node.parent
        if parent is None:
            return False
        return (
            parent.type == "define_directive"
            and uni.get_text() == self.name
            and node == parent.children[1]
        )

    def is_variable_define(self, uni: UNI) -> bool:
        r"""Is variable define.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        parent = node.parent
        if parent is None:
            return False
        return (
            parent.type == "variable_assignment"
            and uni.get_text() == self.name
            and node == parent.children[0]
        )

    def is_target_define(self, uni: UNI) -> bool:
        r"""Is target define.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        parent = node.parent
        if parent is None:
            return False
        return parent.type == "targets" and uni.get_text() == self.name

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        return self.is_define(uni)

    @staticmethod
    def uni2document(uni: UNI) -> str:
        r"""Uni2document.

        :param uni:
        :type uni: UNI
        :rtype: str
        """
        node = uni.node
        parent = node.parent
        if parent is None:
            raise TypeError
        if parent.type == "targets":
            parent = parent.parent
            if parent is None:
                raise TypeError
        return f"""<{uni.uri}>
```make
{UNI.node2text(parent)}
```"""


@dataclass(init=False)
class ReferenceFinder(RepeatedTargetFinder):
    r"""Referencefinder."""

    def __init__(self, node: Node) -> None:
        r"""Init.

        :param node:
        :type node: Node
        :rtype: None
        """
        super().__init__()
        self.name = UNI.node2text(node)
        parent = node.parent
        if parent is None:
            raise TypeError
        if parent.type == "define_directive":
            self.is_reference = self.is_function_reference
        elif parent.type == "variable_assignment":
            self.is_reference = self.is_variable_reference
        elif parent.type == "prerequisites":
            self.is_reference = self.is_target_reference
        else:
            raise NotImplementedError

    def is_function_reference(self, uni: UNI) -> bool:
        r"""Is function reference.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        parent = node.parent
        if parent is None:
            return False
        return (
            parent.type == "arguments"
            # https://github.com/alemuller/tree-sitter-make/issues/8
            and self.name in UNI.node2text(node).split(",")
        )

    def is_variable_reference(self, uni: UNI) -> bool:
        r"""Is variable reference.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        parent = node.parent
        if parent is None:
            return False
        return (
            parent.type == "variable_reference" and uni.get_text() == self.name
        )

    def is_target_reference(self, uni: UNI) -> bool:
        r"""Is target reference.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        node = uni.node
        parent = node.parent
        if parent is None:
            return False
        return parent.type == "targets" and uni.get_text() == self.name

    def __call__(self, uni: UNI) -> bool:
        r"""Call.

        :param uni:
        :type uni: UNI
        :rtype: bool
        """
        return self.is_reference(uni)


DIAGNOSTICS_FINDER_CLASSES = [
    ErrorFinder,
    MissingFinder,
    InvalidPathFinder,
    RepeatedTargetFinder,
]
