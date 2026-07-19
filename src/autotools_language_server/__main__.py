r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""

from . import __name__ as NAME
from . import __version__


def main() -> None:
    r"""Parse arguments and provide shell completions."""
    from .server import AutoconfLanguageServer

    AutoconfLanguageServer(NAME, __version__).start_io()


if __name__ == "__main__":
    main()
