from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from rich.text import Text
from textual import events
from textual.app import ComposeResult, RenderResult
from textual.containers import HorizontalGroup, Horizontal
from textual.reactive import reactive
from textual.widget import Widget

from termos.components.window import Window

if TYPE_CHECKING:
    from termos.main import TermOS


class Clock(Widget):
    time = reactive(str)

    def __init__(self) -> None:
        """Initialize the clock widget."""
        super().__init__()

    def on_mount(self) -> None:
        """Start updating the time every second."""
        self.update_time()  # Initial update
        self.set_interval(1, self.update_time)  # Update every second

    def update_time(self) -> None:
        """Fetch the current time and update the display."""
        self.time = datetime.now().strftime('%H:%M:%S\n%d/%m/%y')

    def render(self) -> RenderResult:
        return self.time


class StartButton(Widget):
    def render(self) -> RenderResult:
        return '╭─╮\n╰─╯'

    async def on_click(self) -> None:
        await self.run_action('app.command_palette')


class WindowTab(Widget):
    italicised = reactive(False)

    def __init__(self, window: Window) -> None:
        super().__init__()
        self.window = window

    def on_mount(self) -> None:
        def set_italicised(minimised: bool):
            self.italicised = minimised

        self.watch(self.window, 'minimised', set_italicised)

    def render(self) -> RenderResult:
        parts = []
        if self.window.icon is not None:
            parts.append(Text(self.window.icon))
        if self.window.title is not None:
            parts.append(Text(
                self.window.title,
                style='italic' if self.italicised else ''
            ))
        return Text(' ').join(parts or [Text('...')])

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
