from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button

class MainFolderPane(Container):
    """A pane that contains the 'Main Folder' taskbar buttons."""

    def compose(self) -> ComposeResult:
        """Create taskbar-style buttons inside a horizontal layout."""
        with Horizontal(id="taskbar-options"):
            yield Button("Main Folder", id="mfbtn")
            yield Button("Bin", id="bbtn")
            yield Button("Settings", id="sbtn")