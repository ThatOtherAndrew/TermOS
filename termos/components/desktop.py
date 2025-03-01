from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Label
from textual import on
from pathlib import Path


class SubFolderPane(VerticalScroll):
    """A pane that dynamically lists .txt files as buttons."""

    def __init__(self) -> None:
        super().__init__()
        self.id = "subfolder-pane"  # Assign an ID for easy styling/querying

    def list_text_files(self) -> None:
        """Read all .txt files from 'mainFolder' and display them as buttons."""
        folder_path = Path("C:\\Users\\a1523\\Desktop\\HackLondon\\termos\\components\\mainFolder")  # Use Path for platform-independent handling
        self.remove_children()  # Clear previous file list

        if not folder_path.exists() or not folder_path.is_dir():
            self.mount(Label("Folder 'mainFolder' not found."))
            return

        text_files = [file for file in folder_path.glob("*.txt")]  # Use Path.glob to find .txt files

        if text_files:
            for file in text_files:
                safe_id = f"file-{file.stem}"  # Use file.stem (filename without extension) and replace spaces
                self.mount(Button(file.name, id=safe_id))  # Use the cleaned ID
        else:
            self.mount(Label("No text files found."))

class MainFolderPane(Container):
    """A pane that contains the 'Main Folder' taskbar buttons and file list display."""

    def __init__(self) -> None:
        super().__init__()
        self.file_list_pane = SubFolderPane()  # Create the file list pane but don't yield it yet

    def compose(self) -> ComposeResult:
        """Create taskbar-style buttons and a container for the file list."""
        with Horizontal(id="taskbar-options"):
            yield Button("Main Folder", id="mfbtn")
            yield Button("Bin", id="bbtn")
            yield Button("Settings", id="sbtn")

    @on(Button.Pressed, "#mfbtn")
    def show_file_list(self) -> None:
        """Handle Main Folder button click and list .txt files."""
        self.mount(self.file_list_pane)
        self.file_list_pane.list_text_files()  # Refresh file list

        # Ensure the pane is mounted *only* if it isn't already added
        if not self.file_list_pane.parent:
            self.call_after_refresh(self.mount, self.file_list_pane)
