from textual.app import ComposeResult
from textual.containers import Center, HorizontalScroll
from textual.widgets import TextArea, Button, Label

from termos.apps import OSApp


class NotesApp(OSApp):
    """A Notes App Widget for the OS."""

    NAME = 'Notes'
    ICON = '📝'
    # language=SCSS
    DEFAULT_CSS = '''
    TextArea {
        width: auto;
    }
    '''

    def content(self) -> ComposeResult:
        with Center():
            yield Label('untitled.txt')
        yield TextArea()
        with HorizontalScroll():
            yield Button('Save', variant='primary')
            yield Button('Save As...', variant='default')
