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
