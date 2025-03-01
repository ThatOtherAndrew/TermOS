from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

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


class WindowTab(Widget):
    def __init__(self, window: Window) -> None:
        super().__init__()
        self.window = window

    def render(self) -> RenderResult:
        return ' '.join(filter(None, [self.window.icon, self.window.title]))


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
