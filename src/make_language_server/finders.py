r"""Finders
===========
"""

import os
from dataclasses import dataclass

from lsp_tree_sitter import UNI
from lsp_tree_sitter.finders import (
    ErrorFinder,
    QueryFinder,
    RepeatedFinder,
)
from lsprotocol.types import DiagnosticSeverity
from tree_sitter import Node, Tree

from .utils import get_query, parser


@dataclass(init=False)
class InvalidPathFinder(QueryFinder):
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
        query = get_query("include")
        super().__init__(query, message, severity)

    def capture2uni(self, capture: tuple[Node, str], uri: str) -> UNI | None:
        r"""Capture2uni.

        :param capture:
        :type capture: tuple[Node, str]
        :param uri:
        :type uri: str
        :rtype: UNI | None
        """
        node, label = capture
        uni = UNI(uri, node)
        return (
            uni
            if label == "path" and not os.path.isfile(uni.get_path())
            else None
        )


@dataclass
class RepeatedTargetFinder(RepeatedFinder):
    r"""Repeatedtargetfinder."""

    message: str = "{{uni.get_text()}}: is repeated on {{_uni}}"
    severity: DiagnosticSeverity = DiagnosticSeverity.Warning

    def __post_init__(self) -> None:
        r"""Post init.

        :rtype: None
        """

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
        return parser.parse(code)

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
        self.is_define = lambda _: False
        if parent.type == "arguments":
            self.is_define = self.is_function_define
            # https://github.com/alemuller/tree-sitter-make/issues/8
            self.name = UNI.node2text(node).split(",")[0]
        elif node.type == "word" and (
            parent.type == "variable_reference"
            or parent.parent is not None
            and parent.parent.type
            in {"export_directive", "unexport_directive"}
        ):
            self.is_define = self.is_variable_define
        elif parent.type == "prerequisites":
            self.is_define = self.is_target_define

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
        self.is_reference = lambda _: False
        if parent.type == "define_directive":
            self.is_reference = self.is_function_reference
        elif parent.type == "variable_assignment":
            self.is_reference = self.is_variable_reference
        elif parent.type == "prerequisites":
            self.is_reference = self.is_target_reference

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
            uni.get_text() == self.name
            and node.type == "word"
            and (
                parent.type == "variable_reference"
                or parent.parent is not None
                and parent.parent.type
                in {"export_directive", "unexport_directive"}
            )
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
    InvalidPathFinder,
    RepeatedTargetFinder,
]
