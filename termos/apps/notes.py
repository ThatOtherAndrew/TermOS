from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import TextArea, Button, Label

from termos.apps import OSApp


class NotesApp(OSApp):
    """A Notes App Widget for the OS."""

    NAME = "Notes"
    ICON = "📝"

    def content(self) -> ComposeResult:
        with Vertical():
            yield Label("Notes App", classes="title")
            yield TextArea(id="note_area")
            yield Button("Save Note", id="save_button")
