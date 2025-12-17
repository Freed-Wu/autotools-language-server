r"""Finders
===========
"""

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from lsp_tree_sitter import UNI
from lsp_tree_sitter.finders import (
    ErrorFinder,
    QueryFinder,
    RepeatedFinder,
)
from lsprotocol.types import (
    DiagnosticSeverity,
    DocumentSymbol,
    SymbolKind,
)
from tree_sitter import Node, Tree

from .utils import get_query, parser

if TYPE_CHECKING:
    from lsprotocol.types import Range


@dataclass(init=False)
class InvalidPathFinder(QueryFinder):
    r"""Invalidpathfinder."""

    def __init__(
        self,
        message: str = "{{uni.text}}: no such file",
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

    def capture2uni(
        self, label: str, nodes: list[Node], uri: str
    ) -> UNI | None:
        r"""Capture2uni.

        :param label:
        :type label: str
        :param nodes:
        :type nodes: list[Node]
        :param uri:
        :type uri: str
        :rtype: UNI | None
        """
        uni = UNI(nodes[0], uri)
        return (
            uni if label == "path" and not os.path.isfile(uni.path) else None
        )


@dataclass
class RepeatedTargetFinder(RepeatedFinder):
    r"""Repeatedtargetfinder."""

    message: str = "{{uni.text}}: is repeated on {{_uni}}"
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
            text = uni.text
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
        self.name = UNI(node).text
        parent = node.parent
        if parent is None:
            raise TypeError
        self.is_define = lambda _: False
        if parent.type == "arguments":
            self.is_define = self.is_function_define
            # https://github.com/alemuller/tree-sitter-make/issues/8
            self.name = UNI(node).text.split(",")[0]
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
            and uni.text == self.name
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
            and uni.text == self.name
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
        return parent.type == "targets" and uni.text == self.name

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
{UNI(parent).text}
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
        self.name = UNI(node).text
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
            and self.name in UNI(node).text.split(",")
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
            uni.text == self.name
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
        return parent.type == "targets" and uni.text == self.name

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


def _node_to_range(node: Node, uri: str) -> "Range":
    r"""Convert tree-sitter node to LSP Range.

    :param node:
    :type node: Node
    :param uri:
    :type uri: str
    :rtype: Range
    """
    from lsprotocol.types import Position, Range

    return Range(
        start=Position(
            line=node.start_point[0],
            character=node.start_point[1],
        ),
        end=Position(
            line=node.end_point[0],
            character=node.end_point[1],
        ),
    )


class DocumentSymbolFinder:
    r"""Finder for document symbols (targets, variables, functions)."""

    def __init__(self) -> None:
        r"""Init."""
        from tree_sitter import QueryCursor

        self.query = get_query("symbols")
        self.cursor = QueryCursor(self.query)

    @staticmethod
    def _is_descendant_of(node: Node, container: Node) -> bool:
        r"""Check if node is a descendant of container.

        :param node:
        :type node: Node
        :param container:
        :type container: Node
        :rtype: bool
        """
        current = node
        while current is not None:
            if current.id == container.id:
                return True
            current = current.parent
        return False

    def find_all(self, uri: str, tree: Tree) -> list[DocumentSymbol]:
        r"""Find all document symbols in the tree.

        :param uri:
        :type uri: str
        :param tree:
        :type tree: Tree
        :rtype: list[DocumentSymbol]
        """
        symbols: list[DocumentSymbol] = []
        captures = self.cursor.captures(tree.root_node)

        # Collect containers and names separately
        containers: dict[str, list[Node]] = {}
        names: dict[str, list[Node]] = {}

        for capture_name, nodes in captures.items():
            if "." in capture_name:
                # This is a name capture like "target.name"
                names[capture_name] = nodes
            else:
                # This is a container capture like "target", "variable", "function"
                containers[capture_name] = nodes

        # Match each container with its corresponding name
        for symbol_type, container_nodes in containers.items():
            name_key = f"{symbol_type}.name"
            name_nodes = names.get(name_key, [])

            for container in container_nodes:
                # Find the name node that belongs to this container
                matching_name = None
                for name_node in name_nodes:
                    if self._is_descendant_of(name_node, container):
                        matching_name = name_node
                        break

                if matching_name is None:
                    continue

                # Determine symbol kind based on type
                if symbol_type == "target":
                    kind = SymbolKind.Function
                elif symbol_type == "variable":
                    kind = SymbolKind.Variable
                elif symbol_type == "function":
                    kind = SymbolKind.Function
                else:
                    kind = SymbolKind.Variable

                # Get the name text
                name = (
                    matching_name.text.decode("utf-8")
                    if matching_name.text
                    else ""
                )

                # Skip special targets (like .PHONY)
                if name.startswith(".") and name.isupper():
                    continue

                symbol = DocumentSymbol(
                    name=name,
                    kind=kind,
                    range=_node_to_range(container, uri),
                    selection_range=_node_to_range(matching_name, uri),
                )
                symbols.append(symbol)

        return symbols
