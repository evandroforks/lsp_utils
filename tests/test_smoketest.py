from LSP.plugin.core.typing import cast, Generator
from .setup import TextDocumentTestCase

try:
    from LSP.plugin.session_view import SessionView
    ST3 = False
except ImportError:
    ST3 = True


class PyrightSmokeTests(TextDocumentTestCase):

    def test_set_and_get(self) -> Generator:
        if ST3:
            error_region_key = 'lsp_error'
        else:
            session_view = cast(SessionView, self.session.session_view_for_view_async(self.view))
            self.assertIsNotNone(session_view)
            error_region_key = session_view.diagnostics_key(1, False)
        error_regions = yield lambda: self.view.get_regions(error_region_key)
        self.assertEqual(len(error_regions), 1)
        region = error_regions[0]
        self.assertEqual(region.a, 11)
        self.assertEqual(region.b, 31)
        self.view.window().run_command('show_panel', {"panel": "console", "toggle": True})
