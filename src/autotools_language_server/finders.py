r"""Finders
===========
"""
import os

from lsprotocol.types import DiagnosticSeverity
from tree_sitter import Node, Tree

from .parser import parse as _parse
from .tree_sitter_lsp import UNI, Finder
from .tree_sitter_lsp.finders import RepeatedFinder


class InvalidPathFinder(Finder):
    r"""Invalidpathfinder."""

    def __init__(
        self,
        message: str = "{{uni.get_text()}}: no such file",
        severity: DiagnosticSeverity = DiagnosticSeverity.Error,
    ) -> None:
        r"""Init.

        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)

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
                and option != "-include"
                and not os.path.isfile(path)
            )
        return False


class RepeatedTargetFinder(RepeatedFinder):
    r"""Repeatedtargetfinder."""

    def __init__(
        self,
        message: str = "{{uni.get_text()}}: is repeated on {{_uni}}",
        severity: DiagnosticSeverity = DiagnosticSeverity.Warning,
    ) -> None:
        r"""Init.

        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__(message, severity)

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
        return _parse(code)

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
