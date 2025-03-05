from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from textual import events
from textual.app import ComposeResult, RenderResult
from textual.containers import HorizontalGroup, Horizontal
from textual.reactive import reactive
from textual.widget import Widget

from termos.components.quick_settings import QuickSettings
from termos.components.start_menu import StartMenu
from termos.components.window import Window

if TYPE_CHECKING:
    from termos.termos import TermOS


class Clock(Widget):
    time = reactive(str)

    def on_mount(self) -> None:
        self.update_time()  # Initial update
        self.set_interval(1, self.update_time)  # Update every second

    def update_time(self) -> None:
        """Fetch the current time and update the display."""
        self.time = datetime.now().strftime('%H:%M:%S\n%d/%m/%y')

    def render(self) -> RenderResult:
        return self.time

    def on_click(self, event: events.Click) -> None:
        if event.button == 1:
            quick_settings = self.app.query_one(QuickSettings)
            quick_settings.visible = not quick_settings.visible


class StartButton(Widget):
    def render(self) -> RenderResult:
        return '╭─╮\n╰─╯'

    async def on_click(self, event: events.Click) -> None:
        if event.button == 1:
            start_menu = self.app.query_one(StartMenu)
            start_menu.visible = not start_menu.visible
        elif event.button == 3:
            await self.run_action('app.command_palette')


class WindowTab(Widget):
    def __init__(self, window: Window) -> None:
        super().__init__()
        self.window = window

    def on_mount(self) -> None:
        def set_minimised(minimised: bool):
            self.set_class(minimised, 'minimised')

        self.watch(self.window, 'minimised', set_minimised)

    def render(self) -> RenderResult:
        parts = []
        if self.window.icon is not None:
            parts.append(self.window.icon)
        if self.window.title is not None:
            parts.append(self.window.title)
        return ' '.join(parts or ['...'])

    def on_click(self) -> None:
        self.window.minimised = not self.window.minimised


class Taskbar(HorizontalGroup):
    app: TermOS
    windows = reactive(list[Window], recompose=True)

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        yield StartButton()

        with Horizontal(classes='tabs-container'):
            for window in self.windows:
                yield WindowTab(window)

        yield Clock()

    def _on_mouse_scroll_down(self, event: events.MouseScrollDown) -> None:
        if self.allow_horizontal_scroll:
            self._clear_anchor()
            if self._scroll_right_for_pointer(animate=True):
                event.stop()
                event.prevent_default()

    def _on_mouse_scroll_up(self, event: events.MouseScrollUp) -> None:
        if self.allow_horizontal_scroll:
            self._clear_anchor()
            if self._scroll_left_for_pointer(animate=True):
                event.stop()
                event.prevent_default()
