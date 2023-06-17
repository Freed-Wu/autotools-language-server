r"""Test api"""
from autoconf_language_server.api import init_document


class Test:
    r"""Test."""

    @staticmethod
    def test_init_document() -> None:
        r"""Test init document.

        :rtype: None
        """
        assert len(init_document().get("AC_INIT", "").splitlines()) > 1
