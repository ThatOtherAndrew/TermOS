from textual.widget import Widget
from textual.widgets import TextArea, Button, Static
from textual.containers import Vertical


class Notes(Widget):
    """A Notes App Widget for the OS."""

    def compose(self):
        yield Vertical(
            Static("Notes App", classes="title"),
            TextArea(id="note_area"),
            Button("Save Note", id="save_button"),
        )