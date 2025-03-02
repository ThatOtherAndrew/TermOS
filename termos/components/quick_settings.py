from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.geometry import Offset
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import Select, Label, Rule, Button

if TYPE_CHECKING:
    from termos.main import TermOS


class QuickSettings(Widget):
    app: TermOS

    visible = var(False, init=False)

    def __init__(self) -> None:
        super().__init__()
        self.styles.display = 'none'

    def compose(self) -> ComposeResult:
        yield Label(Text('Quick Settings', style='bold'), classes='heading')
        yield Rule()
        with HorizontalGroup():
            yield Label('Theme: ')
            yield Select(
                ((key, key) for key in self.app.available_themes),
                allow_blank=False,
                value=self.app.current_theme.name,
            )
        yield Label(f'Themes installed: {len(self.app.available_themes)}', classes='muted')
        yield Rule()
        yield Button('Restart', variant='warning', id='restart')
        yield Button('Power Off', variant='error', id='poweroff')

    def watch_visible(self, new: bool) -> None:
        if new:
            self.styles.offset = (45, 0)
            self.styles.display = 'block'
            self.focus()
            self.animate('offset', value=Offset(), duration=0.5, easing='out_quad')
        else:
            def hide() -> None:
                self.styles.display = 'none'
            self.animate('offset', value=Offset(45), duration=0.5, easing='in_quad', on_complete=hide)

    def on_select_changed(self, message: Select.Changed) -> None:
        self.app.theme = message.value

    async def on_button_pressed(self, message: Button.Pressed) -> None:
        for process in self.app.processes:
            await process.kill()
        if message.button.id == 'poweroff':
            self.app.exit()
        elif message.button.id == 'restart':
            self.app.exit(result=True)
