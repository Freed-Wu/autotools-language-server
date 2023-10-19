r"""Test documents"""
from autotools_language_server.documents import get_document


class Test:
    r"""Test."""

    @staticmethod
    def test_get_document() -> None:
        r"""Test get document.

        :rtype: None
        """
        assert len(get_document().get("AC_INIT", "")[0].splitlines()) > 1
        assert len(get_document().get("CURDIR", "")[0].splitlines()) > 1
