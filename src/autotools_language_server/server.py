r"""Server
==========
"""

import os

from lsp_tree_sitter.completer import SchemaCompleter
from lsp_tree_sitter.server import TreeSitterLanguageServer
from tree_sitter import Language, Parser
from tree_sitter_autoconf import language as get_language_ptr


class AutoconfLanguageServer(TreeSitterLanguageServer):
    def __init__(self, *args, **kwargs) -> None:
        parser = Parser()
        language = Language(get_language_ptr())
        parser.language = language

        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        code_file = os.path.join(assets_path, "jq", "main.jq")
        schema_file = os.path.join(assets_path, "json", "autoconf.json")
        schema_completer = SchemaCompleter.from_files(code_file, schema_file)

        super().__init__(
            parser,
            (),
            (schema_completer,),
            *args,
            **kwargs,
        )
