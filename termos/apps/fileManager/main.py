from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, HorizontalScroll
from textual.widget import Widget
from textual.widgets import TextArea, Button, Label, Static

from termos.apps import OSApp

if TYPE_CHECKING:
    from termos.main import TermOS



class BinWidget(Widget):
    """Displays buttons for each .txt file in the main folder and shows file content when clicked."""

    def __init__(self):
        super().__init__()
        self.root = Path(os.environ['TEMP']) / 'TermOS'
        self.main_folder = self.root / 'mainFolder'
        self.bin_folder = self.root / 'Bin'
        self.main_folder.mkdir(parents=True, exist_ok=True)  # ✅ Ensure folder exists
        self.bin_folder.mkdir(parents=True, exist_ok=True)  # ✅ Ensure folder exists
        self.file_content_display = Static(id="file-content")  # ✅ Area to display file content
        self.selected_file = None

    def compose(self) -> ComposeResult:
        """Dynamically create buttons for each .txt file in mainFolder."""
        yield Label("🚮Bin")

        files = list(self.bin_folder.glob("*.txt"))  # ✅ Get all .txt files

        if files:
            for file in files:
                yield Button(file.name, id=f"file-{file.stem}", classes="file-btn")  # ✅ Create file buttons
        else:
            yield Label("No .txt files found.")

        yield self.file_content_display  # ✅ Add file content display area
        yield Button("Back", id="back-btn")  # ✅ Back button
        yield Button("Recover", id="recover-btn")  # ✅ Delete button
        yield Button("Clear", id="clear-btn")  # ✅ Delete button

    @on(Button.Pressed, "#clear-btn")
    def clear_bin(self) -> None:
        """Delete all files in the Bin folder."""
        for file in self.bin_folder.glob("*.txt"):
            file.unlink()  # ✅ Delete file
            self.remove()
            self.parent.mount(FileManagerWidget())  # ✅ Restore FileManager UI


    @on(Button.Pressed, "#back-btn")
    def go_back(self) -> None:
        """Return to FileManagerWidget by removing itself."""
        self.remove()
        self.parent.mount(FileManagerWidget())  # ✅ Restore FileManager UI

    @on(Button.Pressed, "#recover-btn")
    def move_to_bin(self) -> None:
        """Move the selected file to the Bin folder."""
        if self.selected_file:
            self.selected_file.rename(self.main_folder / self.selected_file.name)  # ✅ Move file to Bin
            self.remove()
            self.parent.mount(FileManagerWidget())  # ✅ Restore FileManager UI


    @on(Button.Pressed)
    def display_file_content(self, event: Button.Pressed) -> None:
        """Displays content of the selected .txt file."""
        button = event.button
        if "file-btn" in button.classes:  # ✅ Ensure it's a file button
            self.selected_file = self.bin_folder / str(button.label)  # Get file path

            try:
                content = self.selected_file.read_text(encoding="utf-8")  # ✅ Read file content
                self.file_content_display.update(f"📄 **{button.label}**\n\n{content}")  # ✅ Display content
            except Exception as e:
                self.file_content_display.update(f"❌ Error reading file: {e}")  # Handle errors

class MFWidget(Widget):
    """Displays buttons for each .txt file in the main folder and shows file content when clicked."""

    def __init__(self):
        super().__init__()
        self.root = Path(os.environ['TEMP']) / 'TermOS'
        self.main_folder = self.root / 'mainFolder'
        self.bin_folder = self.root / 'Bin'
        self.main_folder.mkdir(parents=True, exist_ok=True)  # ✅ Ensure folder exists
        self.bin_folder.mkdir(parents=True, exist_ok=True)  # ✅ Ensure folder exists
        self.file_content_display = Static(id="file-content")  # ✅ Area to display file content
        self.selected_file = None

    def compose(self) -> ComposeResult:
        """Dynamically create buttons for each .txt file in mainFolder."""
        yield Label("📂Main Folder")

        files = list(self.main_folder.glob("*.txt"))  # ✅ Get all .txt files

        if files:
            for file in files:
                yield Button(file.name, id=f"file-{file.stem}", classes="file-btn")  # ✅ Create file buttons
        else:
            yield Label("No .txt files found.")

        yield self.file_content_display  # ✅ Add file content display area
        yield Button("Back", id="back-btn")  # ✅ Back button
        yield Button("Delete", id="bin-btn")  # ✅ Delete button


    @on(Button.Pressed, "#back-btn")
    def go_back(self) -> None:
        """Return to FileManagerWidget by removing itself."""
        self.remove()
        self.parent.mount(FileManagerWidget())  # ✅ Restore FileManager UI

    @on(Button.Pressed, "#bin-btn")
    def move_to_bin(self) -> None:
        """Move the selected file to the Bin folder."""
        if self.selected_file:
            self.selected_file.rename(self.bin_folder / self.selected_file.name)  # ✅ Move file to Bin
            self.remove()
            self.parent.mount(FileManagerWidget())  # ✅ Restore FileManager UI


    @on(Button.Pressed)
    def display_file_content(self, event: Button.Pressed) -> None:
        """Displays content of the selected .txt file."""
        button = event.button
        if "file-btn" in button.classes:  # ✅ Ensure it's a file button
            self.selected_file = self.main_folder / str(button.label)  # Get file path

            try:
                content = self.selected_file.read_text(encoding="utf-8")  # ✅ Read file content
                self.file_content_display.update(f"📄 **{button.label}**\n\n{content}")  # ✅ Display content
            except Exception as e:
                self.file_content_display.update(f"❌ Error reading file: {e}")  # Handle errors


class FileManagerWidget(Widget):
    """Main UI for file management with buttons."""

    def compose(self) -> ComposeResult:
        yield Button('Main Folder', variant='primary', id='fmbtn')
        yield Button('Bin', variant='primary', id='binbtn')

    @on(Button.Pressed, "#fmbtn")
    def open_fm(self) -> None:
        """Mount MFWidget when 'Main Folder' is clicked, listing .txt files."""
        self.remove_children()  # ✅ Clear previous widgets
        self.mount(MFWidget())  # ✅ Mount MFWidget (corrected usage!)

    @on(Button.Pressed, "#binbtn")
    def open_bin(self) -> None:
        """Mount BinWidget when 'Bin' is clicked, listing .txt files."""
        self.remove_children()  # ✅ Clear previous widgets
        self.mount(BinWidget())  # ✅ Mount BinWidget (corrected usage!)

class FileManager(OSApp):
    NAME = 'File Manager'
    ICON = '📂'
    DESCRIPTION = 'File management utility'

    @staticmethod
    def launch(os: TermOS) -> None:
        instance = FileManager(os)
        instance.create_window(FileManagerWidget(), 'notepad', width=50, height=20)