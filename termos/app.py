from textual.app import App as TextualApp
from textual.app import ComposeResult
from textual.widgets import Header

from termos.apps import OSApp
from termos.apps.base import tcss_paths
from termos.apps.notes import NotesApp
from termos.components.taskbar import Taskbar


class TermOS(TextualApp):
    CSS_PATH = ["style.tcss", *tcss_paths()]

    def __init__(self):
        super().__init__()
        self.os_apps: list[OSApp] = [NotesApp()]

    def compose(self) -> ComposeResult:
        yield Header()
        yield from self.os_apps
        yield Taskbar()
