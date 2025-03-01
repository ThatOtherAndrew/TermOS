from textual.app import App, ComposeResult
from textual.app import App as TextualApp
from textual.widgets import Header
from termos.components.desktop import MainFolderPane
from termos.apps import App
from termos.components.taskbar import Taskbar


class TermOS(TextualApp):
    CSS_PATH = "style.tcss"

    def __init__(self):
        super().__init__()
        self.os_apps: list[App] = [App('app-foo'), App('app-bar'), App('app-baz')]

    def compose(self) -> ComposeResult:
        yield Header()
        yield MainFolderPane()
        yield Taskbar()
