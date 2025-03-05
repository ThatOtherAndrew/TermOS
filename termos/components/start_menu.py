from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import ListView, ListItem, Label

if TYPE_CHECKING:
    from termos.termos import TermOS


class StartMenu(Widget):
    app: TermOS

    visible = var(False)

    def compose(self) -> ComposeResult:
        with ListView():
            for app in self.app.os_apps:
                with ListItem():
                    yield Label(f'{app.ICON or ' '} {app.NAME}')
                    yield Label(app.DESCRIPTION, classes='description')

    def watch_visible(self, new: bool) -> None:
        self.styles.display = 'block' if new else 'none'
        if new:
            self.children[0].focus()

    def on_list_view_selected(self, message: ListView.Selected) -> None:
        self.visible = False
        self.app.os_apps[message.list_view.index].launch(self.app)
