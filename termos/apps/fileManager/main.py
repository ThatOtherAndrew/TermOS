from __future__ import annotations

from typing import TYPE_CHECKING

from textual import on
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button
from termos.apps.fileManager.fileManager import SubPanes
from termos.apps import OSApp

if TYPE_CHECKING:
    from termos.main import TermOS


class FileManagerWidget(Widget):
    def __init__(self):
        super().__init__()
        subpane_obj = SubPanes()
        self.file_list_pane = subpane_obj.SubFolderPane(self)
        self.bin_list_pane = subpane_obj.BinFolderPane(self)
        self.button_container = self
    def compose(self) -> ComposeResult:
        yield Button("Main Folder", id="mfbtn")
        yield Button("Bin", id="bbtn")

    @on(Button.Pressed, "#mfbtn")
    def show_file_list(self) -> None:
        """Handle Main Folder button click and list .txt files."""
        self.mount(self.file_list_pane)
        self.file_list_pane.list_text_files()
        self.button_container.styles.display = "none"  # ✅ Hide primary buttons

    @on(Button.Pressed, "#bbtn")
    def show_bin_list(self) -> None:
        """Handle Bin button click and list files in the 'Bin' folder."""
        self.mount(self.bin_list_pane)
        self.bin_list_pane.list_bin_files()
        self.button_container.styles.display = "none"  # ✅ Hide primary buttons

    def show_primary_buttons(self) -> None:
        """Restore the primary buttons when the file list is closed."""
        self.button_container.styles.display = "block"  # ✅ Show primary buttons again


class FileManager(OSApp):
    NAME = 'File Manager'
    ICON = '🗂️'
    DESCRIPTION = 'Browse and manage files'

    @staticmethod
    def launch(os: TermOS) -> None:
        instance = FileManager(os)
        instance.create_window(FileManagerWidget(), 'file-manager', width=50, height=20)
