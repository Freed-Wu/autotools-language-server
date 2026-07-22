import os

from autotools_language_server.server import AutoconfLanguageServer as Server

server = Server("")
file = os.path.join(os.path.dirname(__file__), "zathurarc")


class Test:
    @staticmethod
    def test_complete() -> None:
        contents = server.lookup("AC_INIT", kind="macro_name")["AC_INIT"]
        assert len(contents)
