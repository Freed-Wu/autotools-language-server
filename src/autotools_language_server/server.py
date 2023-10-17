r"""Server
==========
"""
import os
import re
from typing import Any, Tuple
from urllib.parse import unquote, urlparse

from lsprotocol.types import (
    INITIALIZE,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_HOVER,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    Diagnostic,
    DiagnosticSeverity,
    DidChangeTextDocumentParams,
    Hover,
    InitializeParams,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
    TextDocumentPositionParams,
)
from pygls.server import LanguageServer

from ._tree_sitter import get_parser
from .diagnostics import diagnostic
from .documents import check_extension, get_document


class AutotoolsLanguageServer(LanguageServer):
    r"""Autotools language server."""

    def __init__(self, *args: Any) -> None:
        r"""Init.

        :param args:
        :type args: Any
        :rtype: None
        """
        super().__init__(*args)
        self.document = {}
        self.parser = get_parser()
        self.tree = self.parser.parse(b"")

        @self.feature(INITIALIZE)
        def initialize(params: InitializeParams) -> None:
            opts = params.initialization_options
            method = getattr(opts, "method", "builtin")
            self.document = get_document(method)  # type: ignore

        @self.feature(TEXT_DOCUMENT_HOVER)
        def hover(params: TextDocumentPositionParams) -> Hover | None:
            r"""Hover.

            :param params:
            :type params: TextDocumentPositionParams
            :rtype: Hover | None
            """
            if not check_extension(
                unquote(urlparse(params.text_document.uri).path)
            ):
                return None
            word = self._cursor_word(
                params.text_document.uri, params.position, True
            )
            if not word:
                return None
            result = self.document.get(word[0])
            if not result:
                return None
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.PlainText, value=result[0]
                ),
                range=word[1],
            )

        @self.feature(TEXT_DOCUMENT_COMPLETION)
        def completions(params: CompletionParams) -> CompletionList:
            r"""Completions.

            :param params:
            :type params: CompletionParams
            :rtype: CompletionList
            """
            if not check_extension(
                unquote(urlparse(params.text_document.uri).path)
            ):
                return CompletionList(is_incomplete=False, items=[])
            word = self._cursor_word(
                params.text_document.uri, params.position, False
            )
            token = "" if word is None else word[0]
            items = [
                CompletionItem(
                    label=x,
                    kind=CompletionItemKind.Function,
                    documentation=self.document[x][0],
                    insert_text=x,
                )
                for x in self.document
                if x.startswith(token)
                and self.document[x][1]
                == check_extension(
                    unquote(urlparse(params.text_document.uri).path)
                )
            ]
            return CompletionList(is_incomplete=False, items=items)

        @self.feature(TEXT_DOCUMENT_DID_OPEN)
        @self.feature(TEXT_DOCUMENT_DID_CHANGE)
        def did_change(params: DidChangeTextDocumentParams) -> None:
            r"""Did change.

            :param params:
            :type params: DidChangeTextDocumentParams
            :rtype: None
            """
            if (
                check_extension(
                    unquote(urlparse(params.text_document.uri).path)
                )
                != "make"
            ):
                return None
            doc = self.workspace.get_document(params.text_document.uri)
            source = doc.source
            self.tree = self.parser.parse(bytes(source, "utf-8"))
            diagnostics = [
                Diagnostic(
                    range=Range(
                        Position(node.start_point[0], node.start_point[1]),
                        Position(node.end_point[0], node.end_point[1]),
                    ),
                    message=message,
                    severity=getattr(DiagnosticSeverity, severity),
                    source="autotools-language-server",
                )
                for node, message, severity in diagnostic(
                    self.tree,
                    os.path.dirname(
                        unquote(urlparse(params.text_document.uri).path)
                    ),
                )
            ]
            self.publish_diagnostics(doc.uri, diagnostics)

    def _cursor_line(self, uri: str, position: Position) -> str:
        r"""Cursor line.

        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :rtype: str
        """
        doc = self.workspace.get_document(uri)
        content = doc.source
        line = content.split("\n")[position.line]
        return str(line)

    def _cursor_word(
        self, uri: str, position: Position, include_all: bool = True
    ) -> Tuple[str, Range] | None:
        r"""Cursor word.

        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :param include_all:
        :type include_all: bool
        :rtype: Tuple[str, Range] | None
        """
        line = self._cursor_line(uri, position)
        cursor = position.character
        for m in re.finditer(r"[^$() ]+", line):
            end = m.end() if include_all else cursor
            if m.start() <= cursor <= m.end():
                word = (
                    line[m.start() : end],
                    Range(
                        Position(position.line, m.start()),
                        Position(position.line, end),
                    ),
                )
                return word
        return None
