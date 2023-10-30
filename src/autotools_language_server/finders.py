r"""Finders
===========
"""
import os
from dataclasses import dataclass

from lsprotocol.types import DiagnosticSeverity
from tree_sitter import Node, Tree
from tree_sitter_languages import get_parser
from tree_sitter_lsp import UNI
from tree_sitter_lsp.finders import (
    ErrorQueryFinder,
    QueryFinder,
    RepeatedFinder,
)

from .utils import get_query


@dataclass(init=False)
class ErrorMakeFinder(ErrorQueryFinder):
    r"""Errormakefinder."""

    def __init__(
        self,
        message: str = "{{uni.get_text()}}: error",
        severity: DiagnosticSeverity = DiagnosticSeverity.Error,
    ) -> None:
        r"""Init.

        :param filetype:
        :type filetype: str
        :param message:
        :type message: str
        :param severity:
        :type severity: DiagnosticSeverity
        :rtype: None
        """
        super().__init__("make", message, severity)


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
            if label == "path" and not os.path.isfile(self.uni2path(uni))
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
class DefinitionFinder(QueryFinder):
    r"""Definitionfinder."""

    def __init__(self, node: Node) -> None:
        r"""Init.

        :param node:
        :type node: Node
        :rtype: None
        """
        self.name = UNI.node2text(node)
        parent = node.parent
        if parent is None:
            raise TypeError
        if parent.type == "arguments":
            self.label = "function"
            # https://github.com/alemuller/tree-sitter-make/issues/8
            self.name = UNI.node2text(node).split(",")[0]
        elif node.type == "word" and (
            parent.type == "variable_reference"
            or parent.parent is not None
            and parent.parent.type
            in {"export_directive", "unexport_directive"}
        ):
            self.label = "variable"
        elif parent.type == "prerequisites":
            self.label = "rule"
        else:
            raise NotImplementedError
        query = get_query("define")
        super().__init__(query)

    def find_all(
        self, uri: str, tree: Tree | None = None, reset: bool = True
    ) -> list[UNI]:
        tree = self.prepare(uri, tree, reset)
        captures = self.query.captures(tree.root_node)
        candidate = None
        unis = []
        for node, label in captures:
            if label == self.label:
                candidate = node
                continue
            if (
                label == f"{self.label}.def"
                and UNI.node2text(node) == self.name
            ):
                unis += [UNI(uri, node)]
        return unis

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
    ErrorMakeFinder,
    InvalidPathFinder,
    RepeatedTargetFinder,
]
