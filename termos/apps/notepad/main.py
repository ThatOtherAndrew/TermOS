from textual.app import ComposeResult
from textual.containers import Center, HorizontalScroll
from textual.widgets import TextArea, Button, Label

from termos.apps import OSApp


class Notepad(OSApp):
    NAME = 'Notepad'
    ICON = '📝'
    DESCRIPTION = 'Simple text editor'

    @staticmethod
    def compose() -> ComposeResult:
        with Center():
            yield Label('<new file>')
        yield TextArea(show_line_numbers=True)
        with HorizontalScroll(classes='buttons'):
            yield Button('Save', variant='primary')
            yield Button('Save As...', variant='default')

    def launch(self) -> None:
        self.create_window(self.compose(), 'notepad', width=50, height=20)
