from __future__ import annotations

from typing import TYPE_CHECKING

import os
from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Horizontal, Container
from textual.widget import Widget
from textual.widgets import Button, Static, Label, Input
from termos.apps.fileManager.fileManager import SubPanes
from termos.apps import OSApp

if TYPE_CHECKING:
    from termos.main import TermOS

class SubPanes:
    def __init__(self) -> None:
        self.root = Path(os.environ['TEMP']) / 'TermOS'
        self.main_folder = self.root / 'mainFolder'
        self.main_folder.mkdir(exist_ok=True)
        self.bin_folder = self.root / 'Bin'
        self.bin_folder.mkdir(exist_ok=True)
    class BinFolderPane(VerticalScroll):
        """A pane that lists files in the 'Bin', allows viewing content, and recovering files."""
        CSS_PATH = "style.tcss"

        def __init__(self, main_folder_pane) -> None:
            super().__init__()
            self.outer_instance = SubPanes()
            self.idSuffix = 0
            self.id = "binfolder-pane"
            self.file_content_display = Static(id="bin-file-content")
            self.main_folder_pane = main_folder_pane  # Reference to MainFolderPane
            self.selected_file = None  # Track selected file
            self.back_button = None  # ✅ Remove hardcoded back button
            self.delete_button = None  # ✅ Remove hardcoded delete button
            self.root_path = self.outer_instance.root
            self.bin_folder = self.outer_instance.bin_folder
            self.main_folder = self.outer_instance.main_folder

        def list_bin_files(self) -> None:
            """Read all files from 'Bin' and display them as buttons."""


            self.remove_children()  # ✅ Clear previous file list
            self.mount(self.file_content_display)  # ✅ Ensure content display exists

            if not self.bin_folder.exists() or not self.bin_folder.is_dir():
                self.mount(Label("Folder 'Bin' not found."))
                return

            bin_files = list(self.bin_folder.iterdir())  # ✅ Get all files

            if bin_files:
                for file in bin_files:
                    self.idSuffix += 1
                    safe_id = f"bin-file-{self.idSuffix}"

                    file_row = Horizontal()  # ✅ Create a row for each file
                    file_button = Button(file.name, id=safe_id)
                    file_button.path = file  # ✅ Store file path in button
                    recover_button = Button("Recover", id=f"recover-{self.idSuffix}")

                    recover_button.path = file  # ✅ Store file path in the recover button
                    self.mount(file_row)
                    file_row.mount(file_button)
                    file_row.mount(recover_button)

                    self.mount(file_row)

            else:
                self.mount(Label("No files in Bin."))
            self.add_back_button()  # ✅ Add back button after listing files
            self.add_delete_button()  # ✅ Add delete button after listing files

        def add_delete_button(self) -> None:
            """Ensure the 'Delete' button is always interactive and unique."""
            self.idSuffix += 1
            if self.delete_button:
                self.delete_button.remove()  # ✅ Remove old delete button before re-adding

            self.delete_button = Button("Delete", id=f"bin-delete-btn-{self.idSuffix}")
            self.mount(self.delete_button)  # ✅ Add new delete button

        def add_back_button(self) -> None:
            """Ensure the 'Back' button is always interactive and unique."""
            self.idSuffix += 1
            if self.back_button:
                self.back_button.remove()  # ✅ Remove previous button before re-adding
            self.back_button = Button("Back", id=f"bin-back-btn-{self.idSuffix}")  # ✅ Unique ID for each session
            self.mount(self.back_button)

        @on(Button.Pressed)
        def handle_bin_button_click(self, event: Button.Pressed) -> None:
            """Handle button clicks (Back, Recover, Delete, or file selection)."""
            button = event.button

            if button.id.startswith("bin-back-btn"):
                self.close_bin_view()

            elif button.id.startswith("recover-") and hasattr(button, "path"):
                self.recover_file(button.path)  # ✅ Recover file

            elif button.id.startswith("bin-delete-btn"):  # ✅ Detect delete button click
                self.delete_file()  # ✅ Call delete method

            elif hasattr(button, "path"):
                self.selected_file = button.path  # ✅ Store selected file
                self.display_bin_file_content(button)

        def display_bin_file_content(self, button: Button) -> None:
            """Display the content of the clicked file from Bin."""
            file_path = button.path
            try:
                content = file_path.read_text(encoding="utf-8")
                self.file_content_display.update(content)
            except Exception as e:
                self.file_content_display.update(f"Error reading file: {e}")

        def delete_file(self) -> None:
            """Delete all files permanently from the 'Bin' folder and refresh UI."""
            try:
                deleted_files = list(self.bin_folder.iterdir())  # ✅ Get all files before deleting

                if not deleted_files:
                    self.file_content_display.update("Bin is already empty.")
                    return  # ✅ Exit if there are no files to delete

                for file in deleted_files:
                    os.remove(file)  # ✅ Delete each file

                self.file_content_display.update("Deleted all files permanently.")

                # ✅ Refresh the bin file list immediately after deletion
                self.list_bin_files()

            except Exception as e:
                self.file_content_display.update(f"Error deleting files: {e}")

        def recover_file(self, file_path: Path) -> None:
            """Recover the selected file back to 'mainFolder'."""
            destination = self.main_folder / file_path.name

            try:
                file_path.rename(destination)
                self.file_content_display.update(f"Recovered {file_path.name} to Main Folder.")

                # ✅ Fix: Refresh list and ensure the back button is restored
                self.call_later(self.refresh_bin_list)

            except Exception as e:
                self.file_content_display.update(f"Error recovering file: {e}")

        def refresh_bin_list(self) -> None:
            """Refresh the file list and re-create the back button after recovery."""
            self.list_bin_files()  # ✅ Refresh the bin file list

        def close_bin_view(self) -> None:
            """Close the Bin file list and show the primary buttons again."""
            self.remove()  # ✅ Remove Bin pane
            self.main_folder_pane.show_primary_buttons()  # ✅ Restore main buttons


    class SubFolderPane(VerticalScroll):
        """A pane that dynamically lists .txt files as buttons, allows creating new files, and displays content."""
        CSS_PATH = "style.tcss"

        def __init__(self, main_folder_pane) -> None:
            super().__init__()
            self.cancel_button = None
            self.save_button = None
            self.outer_instance = SubPanes()
            self.id = "subfolder-pane"
            self.file_content_display = Static(id="file-content")
            self.main_folder_pane = main_folder_pane  # Reference to MainFolderPane
            self.button_row = Horizontal()  # Store reference to button row
            self.main_folder = self.outer_instance.main_folder
            self.bin_path = self.outer_instance.bin_folder
            self.root = self.outer_instance.root
            self.id_suffix = 0
            self.input_dialog = None  # Store input fields for new file creation
            self.back_button = None  # ✅ Remove hardcoded back button
            self.new_file_button = None

        def list_text_files(self) -> None:
            self.remove_children()  # ✅ Clear previous file list
            self.mount(self.file_content_display)  # ✅ Ensure content display exists

            if not self.main_folder.exists() or not self.main_folder.is_dir():
                self.mount(Label("Folder 'Bin' not found."))
                return

            main_files = list(self.main_folder.iterdir())  # ✅ Get all files

            if main_files:
                for file in main_files:
                    self.id_suffix+= 1
                    safe_id = f"bin-file-{self.id_suffix}"

                    file_row = Horizontal()  # ✅ Create a row for each file
                    file_button = Button(file.name, id=safe_id)
                    file_button.path = file  # ✅ Store file path in button
                    bin_button = Button("Bin", id=f"bin-btn-{self.id_suffix}")

                    bin_button.path = file  # ✅ Store file path in the recover button
                    self.mount(file_row)
                    file_row.mount(file_button)
                    file_row.mount(bin_button)


            else:
                self.mount(Label("No files in Bin."))
            self.add_back_button()  # ✅ Add back button after listing files
            self.add_new_file_button()  # ✅ Add delete button after listing files

        def add_new_file_button(self) -> None:
            """Ensure the 'Delete' button is always interactive and unique."""
            self.id_suffix += 1
            if self.new_file_button:
                self.new_file_button.remove()  # ✅ Remove old delete button before re-adding
            self.new_file_button = Button("New File", id=f"newfile-btn-{self.id_suffix}")
            self.mount(self.new_file_button)  # ✅ Add new delete button

        def add_back_button(self) -> None:
            """Ensure the 'Back' button is always interactive and unique."""
            self.id_suffix += 1
            if self.back_button:
                self.back_button.remove()
            self.back_button = Button("Back", id=f"back-btn-{self.id_suffix}")
            self.mount(self.back_button)

        def add_save_button(self) -> None:
            """Ensure the 'Save' button is always interactive and unique."""
            self.id_suffix += 1
            if self.save_button:
                self.save_button.remove()  # ✅ Remove previous button before re-adding
            self.save_button = Button("Save", id=f"save-btn-{self.id_suffix}")  # ✅ Unique ID for each session
            self.mount(self.save_button)

        def add_cancel_button(self) -> None:
            """Ensure the 'Cancel' button is always interactive and unique."""
            self.id_suffix += 1
            if self.cancel_button:
                self.back_button.remove()  # ✅ Remove previous button before re-adding
            self.cancel_button = Button("Cancel", id=f"cancel-btn-{self.id_suffix}")  # ✅ Unique ID for each session
            self.mount(self.cancel_button)

        @on(Button.Pressed)
        def handle_button_click(self, event: Button.Pressed) -> None:
            """Handle button clicks (file selection, back, bin, new file)."""
            button = event.button
            if button.id.startswith( "back-btn"):
                self.close_file_list()
            elif button.id.startswith("bin-btn"):
                self.move_file_to_bin(button.path)
            elif button.id.startswith( "newfile-btn"):
                self.show_new_file_dialog()  # ✅ Show input fields for new file
            elif hasattr(button, "path"):
                self.selected_file = button.path  # ✅ Store selected file
                self.display_file_content(button)

        def show_new_file_dialog(self) -> None:
            """Display input fields for new file name and content."""
            self.input_dialog = Container()

            filename_input = Input(id="filename-input", placeholder="Enter file name")
            content_input = Input(id="content-input", placeholder="Enter content")

            # ✅ Set initial text as placeholder (since TextArea lacks placeholder support)
            #content_input.update("Enter file content here...")
            self.mount(self.input_dialog)
            self.input_dialog.mount(Label("Create New File"))
            self.input_dialog.mount(filename_input)
            self.input_dialog.mount(content_input)
            self.add_save_button()
            self.add_cancel_button()
        @on(Button.Pressed)
        def handle_file_creation_buttons(self, event: Button.Pressed) -> None:
            """Handle Save and Cancel actions for file creation."""
            button = event.button
            if button.id.startswith("save-btn"):
                self.save_new_file()
            elif button.id.startswith("cancel-btn"):
                self.close_file_creation_dialog()

        def save_new_file(self) -> None:
            """Save the new file and refresh the file list."""
            filename_input = self.query_one("#filename-input", Input)
            content_input = self.query_one("#content-input", Input)

            filename = filename_input.value.strip()
            content = content_input.value.strip()

            if not filename:
                self.file_content_display.update("❌ Error: File name cannot be empty.")
                return

            # Ensure the file has a .txt extension
            if not filename.endswith(".txt"):
                filename += ".txt"

            new_file_path = self.main_folder / filename

            try:
                # ✅ Write the content to the new file
                new_file_path.write_text(content, encoding="utf-8")
                self.file_content_display.update(f"✅ File '{filename}' created successfully.")

                # ✅ Remove the input dialog after saving
                self.input_dialog.remove()

                # ✅ Refresh the file list to display the new file
                self.list_text_files()

            except Exception as e:
                pass

        def close_file_creation_dialog(self) -> None:
            """Close the file creation dialog."""
            if self.input_dialog:
                self.input_dialog.remove()
                self.input_dialog = None
                self.list_text_files()

        def display_file_content(self, button: Button) -> None:
            """Display the content of the clicked file."""
            file_path = button.path
            try:
                content = file_path.read_text(encoding="utf-8")
                self.file_content_display.update(content)
            except Exception as e:
                self.file_content_display.update(f"Error reading file: {e}")

        def move_file_to_bin(self, file_path: Path) -> None:
            """Recover the selected file back to 'mainFolder'."""
            destination = self.bin_path / file_path.name

            try:
                file_path.rename(destination)
                self.file_content_display.update(f"Moved {file_path.name} to Bin.")

                # ✅ Fix: Refresh list and ensure the back button is restored
                self.call_later(self.refresh_file_list)

            except Exception as e:
                pass

        def refresh_file_list(self) -> None:
            """Refresh the file list and re-create the back button after moving a file."""
            self.list_text_files()

        def close_file_list(self) -> None:
            """Close the file list and show the primary buttons again."""
            self.remove()  # ✅ Remove file list pane
            self.main_folder_pane.show_primary_buttons()  # ✅ Restore primary buttons


class FileManagerWidget(Widget):
    def __init__(self):
        super().__init__()
        self.button_container = self
        self.file_list_pane = None
        self.bin_list_pane = None

    def compose(self) -> ComposeResult:
        yield Button("Main Folder", id="mfbtn")
        yield Button("Bin", id="bbtn")

    @on(Button.Pressed, "#mfbtn")
    def show_file_list(self) -> None:
        """Handle Main Folder button click and list .txt files."""
        if self.file_list_pane is None:  # ✅ Prevent multiple instances
            self.file_list_pane = SubPanes.SubFolderPane(self)

        self.mount(self.file_list_pane)  # ✅ Mount only one instance
        self.file_list_pane.list_text_files()
        self.button_container.styles.display = "none"  # ✅ Hide primary buttons

    @on(Button.Pressed, "#bbtn")
    def show_bin_list(self) -> None:
        """Handle Bin button click and list files in the 'Bin' folder."""
        if self.bin_list_pane is None:  # ✅ Prevent multiple instances
            self.bin_list_pane = SubPanes.BinFolderPane(self)

        self.mount(self.bin_list_pane)  # ✅ Mount only one instance
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
