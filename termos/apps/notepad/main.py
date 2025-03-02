from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Center, HorizontalScroll
from textual.widget import Widget
from textual.widgets import TextArea, Button, Label

from termos.apps import OSApp

if TYPE_CHECKING:
    from termos.main import TermOS


class NotepadWidget(Widget):
    def compose(self) -> ComposeResult:
        with Center():
            yield Label('<new file>')
        yield TextArea(show_line_numbers=True)
        with HorizontalScroll(classes='buttons'):
            yield Button('Save', variant='primary')
            yield Button('Save As...', variant='default')


class Notepad(OSApp):
    NAME = 'Notepad'
    ICON = '📝'
    DESCRIPTION = 'Simple text editor'

    @staticmethod
    def launch(os: TermOS) -> None:
        instance = Notepad(os)
        instance.create_window(NotepadWidget(), 'notepad', width=50, height=20)
