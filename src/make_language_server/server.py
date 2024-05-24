r"""Server
==========
"""

import re
from typing import Any

from lsp_tree_sitter.diagnose import get_diagnostics
from lsp_tree_sitter.finders import PositionFinder
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DEFINITION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_REFERENCES,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    DidChangeTextDocumentParams,
    Hover,
    Location,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
    TextDocumentPositionParams,
)
from pygls.server import LanguageServer

from .finders import (
    DIAGNOSTICS_FINDER_CLASSES,
    DefinitionFinder,
    ReferenceFinder,
)
from .utils import get_schema, parser


class MakeLanguageServer(LanguageServer):
    r"""Make language server."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        r"""Init.

        :param args:
        :type args: Any
        :param kwargs:
        :type kwargs: Any
        :rtype: None
        """
        super().__init__(*args)
        self.trees = {}

        @self.feature(TEXT_DOCUMENT_DID_OPEN)
        @self.feature(TEXT_DOCUMENT_DID_CHANGE)
        def did_change(params: DidChangeTextDocumentParams) -> None:
            r"""Did change.

            :param params:
            :type params: DidChangeTextDocumentParams
            :rtype: None
            """
            document = self.workspace.get_document(params.text_document.uri)
            self.trees[document.uri] = parser.parse(document.source.encode())
            diagnostics = get_diagnostics(
                document.uri,
                self.trees[document.uri],
                DIAGNOSTICS_FINDER_CLASSES,
            )
            self.publish_diagnostics(params.text_document.uri, diagnostics)

        @self.feature(TEXT_DOCUMENT_DEFINITION)
        def definition(params: TextDocumentPositionParams) -> list[Location]:
            r"""Get definition.

            :param params:
            :type params: TextDocumentPositionParams
            :rtype: list[Location]
            """
            document = self.workspace.get_document(params.text_document.uri)
            uni = PositionFinder(params.position).find(
                document.uri, self.trees[document.uri]
            )
            if uni is None:
                return []
            return [
                uni.get_location()
                for uni in DefinitionFinder(uni.node).find_all(
                    document.uri, self.trees[document.uri]
                )
            ]

        @self.feature(TEXT_DOCUMENT_REFERENCES)
        def references(params: TextDocumentPositionParams) -> list[Location]:
            r"""Get references.

            :param params:
            :type params: TextDocumentPositionParams
            :rtype: list[Location]
            """
            document = self.workspace.get_document(params.text_document.uri)
            uni = PositionFinder(params.position).find(
                document.uri, self.trees[document.uri]
            )
            if uni is None:
                return []
            return [
                uni.get_location()
                for uni in ReferenceFinder(uni.node).find_all(
                    document.uri, self.trees[document.uri]
                )
            ]

        @self.feature(TEXT_DOCUMENT_HOVER)
        def hover(params: TextDocumentPositionParams) -> Hover | None:
            r"""Hover.

            :param params:
            :type params: TextDocumentPositionParams
            :rtype: Hover | None
            """
            document = self.workspace.get_document(params.text_document.uri)
            uni = PositionFinder(params.position).find(
                document.uri, self.trees[document.uri]
            )
            if uni is None:
                return None
            text = uni.get_text()
            _range = uni.get_range()
            parent = uni.node.parent
            if parent is None:
                return None
            if parent.type in [
                "prerequisites",
                "variable_reference",
                "arguments",
            ]:
                result = "\n".join(
                    DefinitionFinder.uni2document(uni)
                    for uni in DefinitionFinder(uni.node).find_all(
                        document.uri, self.trees[document.uri]
                    )
                )
                if result != "":
                    return Hover(
                        MarkupContent(MarkupKind.Markdown, result),
                        _range,
                    )
            if parent.type not in [
                "variable_reference",
                "function_call",
                "conditional",
                "ifneq_directive",
                "else_directive",
                "define_directive",
                "include_directive",
            ]:
                return None
            if (
                description := get_schema()
                .get("properties", {})
                .get(text, {})
                .get("description")
            ):
                return Hover(
                    MarkupContent(MarkupKind.Markdown, description),
                    _range,
                )

        @self.feature(TEXT_DOCUMENT_COMPLETION)
        def completions(params: CompletionParams) -> CompletionList:
            r"""Completions.

            .. todo::
                Distinguish different node type without
                ``self._cursor_word()``.

            :param params:
            :type params: CompletionParams
            :rtype: CompletionList
            """
            text, _ = self._cursor_word(
                params.text_document.uri, params.position, False, r"[^$() ]"
            )
            items = [
                CompletionItem(
                    k,
                    kind=CompletionItemKind.Function,
                    documentation=MarkupContent(
                        MarkupKind.Markdown, v.get("description", "")
                    ),
                    insert_text=k,
                )
                for k, v in get_schema().get("properties", {}).items()
                if k.startswith(text)
            ]
            return CompletionList(is_incomplete=False, items=items)

    def _cursor_line(self, uri: str, position: Position) -> str:
        r"""Cursor line.

        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :rtype: str
        """
        document = self.workspace.get_document(uri)
        return document.source.splitlines()[position.line]

    def _cursor_word(
        self,
        uri: str,
        position: Position,
        include_all: bool = True,
        regex: str = r"\w+",
    ) -> tuple[str, Range]:
        """Cursor word.

        :param self:
        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :param include_all:
        :type include_all: bool
        :param regex:
        :type regex: str
        :rtype: tuple[str, Range]
        """
        line = self._cursor_line(uri, position)
        for m in re.finditer(regex, line):
            if m.start() <= position.character <= m.end():
                end = m.end() if include_all else position.character
                return (
                    line[m.start() : end],
                    Range(
                        Position(position.line, m.start()),
                        Position(position.line, end),
                    ),
                )
        return (
            "",
            Range(Position(position.line, 0), Position(position.line, 0)),
        )
