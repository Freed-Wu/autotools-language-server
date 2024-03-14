r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime

from . import FILETYPE, __version__
from . import __name__ as NAME

try:
    import shtab
except ImportError:
    from . import _shtab as shtab

NAME = NAME.replace("_", "-")
VERSION = rf"""{NAME} {__version__}
Copyright (C) {datetime.now().year}
Written by Wu Zhenyu
"""
EPILOG = """
Report bugs to <wuzhenyu@ustc.edu>.
"""


def get_parser() -> ArgumentParser:
    r"""Get a parser for unit test."""
    parser = ArgumentParser(
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )
    shtab.add_argument_to(parser)
    parser.add_argument("--version", version=VERSION, action="version")
    parser.add_argument(
        "--generate-schema",
        choices=FILETYPE.__args__,  # type: ignore
        help="generate schema in an output format",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "yaml", "toml"],
        default="json",
        help="output format: %(default)s",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="generated json, yaml's indent, ignored by toml: %(default)s",
    )
    parser.add_argument(
        "--color",
        choices=["auto", "always", "never"],
        default="auto",
        help="when to display color, default: %(default)s",
    )
    parser.add_argument(
        "--check",
        nargs="*",
        default={},
        help="check file's errors and warnings",
    ).complete = shtab.FILE  # type: ignore
    return parser


def main() -> None:
    r"""Parse arguments and provide shell completions."""
    args = get_parser().parse_args()

    if args.generate_schema or args.check:
        from lsp_tree_sitter.diagnose import check
        from lsp_tree_sitter.utils import pprint
        from tree_sitter_languages import get_parser as _get_parser

        from .finders import DIAGNOSTICS_FINDER_CLASSES
        from .misc import get_schema

        if args.generate_schema:
            pprint(get_schema(args.generate_schema), indent=args.indent)
        parser = _get_parser("make")
        exit(
            check(
                args.check,
                parser.parse,
                DIAGNOSTICS_FINDER_CLASSES,
                None,
                args.color,
            )
        )

    from .server import MakeLanguageServer

    MakeLanguageServer(NAME, __version__).start_io()


if __name__ == "__main__":
    main()
