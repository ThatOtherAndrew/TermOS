from __future__ import annotations

from typing import TYPE_CHECKING

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button

if TYPE_CHECKING:
    from termos.main import TermOS

class DTPane(Container):
    """A pane that contains the 'Main Folder' taskbar buttons and file list display."""

    app: TermOS

    def compose(self) -> ComposeResult:
        """Create taskbar-style buttons and a container for the file list."""
        yield Button("FolderManager", id="fmbtn")
        yield Button("NotePad", id="npbtn")
            #yield Button("Settings", id="sbtn")

    @on(Button.Pressed, "#npbtn")
    def open_np(self) -> None:
        """Handle Notepad button click and launch the Notepad app."""
        self.app.os_apps[0].launch(self.app)

    @on(Button.Pressed, "#fmbtn")
    def open_fm(self) -> None:
        self.app.os_apps[1].launch(self.app)
