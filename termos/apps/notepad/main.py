from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Center
from textual.widget import Widget
from textual.widgets import TextArea, Label, Select

from termos.apps import OSApp

if TYPE_CHECKING:
    from termos.termos import TermOS


class NotepadWidget(Widget):
    def compose(self) -> ComposeResult:
        with Center():
            yield Label('<new file>')
        editor = TextArea.code_editor()
        yield editor
        yield Select(
            ((lang, lang) for lang in editor.available_languages),
            prompt='Select language...',
        )

    def on_select_changed(self, message: Select.Changed) -> None:
        self.query_one(TextArea).language = message.value


class Notepad(OSApp):
    NAME = 'Notepad'
    ICON = '📝'
    DESCRIPTION = 'Simple text editor'

    @staticmethod
    def launch(os: TermOS) -> None:
        instance = Notepad(os)
        instance.create_window(NotepadWidget(), 'notepad', width=50, height=20)
