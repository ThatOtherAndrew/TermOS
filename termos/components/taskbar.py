from __future__ import annotations

import time

from typing import TYPE_CHECKING

from textual import events
from textual.app import ComposeResult, RenderResult
from textual.containers import ScrollableContainer
from textual.widget import Widget

from termos.apps import App

if TYPE_CHECKING:
    from termos.app import TermOS


class Clock(Widget):
    def __init__(self) -> None:
        """Initialize the clock widget."""
        super().__init__()
        self.time = '00:00:00'

    def on_mount(self) -> None:
        """Start updating the time every second."""
        self.update_time()  # Initial update
        self.set_interval(1, self.update_time)  # Update every second

    def update_time(self) -> None:
        """Fetch the current time and update the display."""
        current_time = time.localtime()
        self.time = f"{current_time.tm_hour:02}:{current_time.tm_min:02}:{current_time.tm_sec:02}"  # Update the UI
        self.refresh()  # Refresh the widget to reflect the change

    def render(self) -> RenderResult:
        return self.time


class StartButton(Widget):
    def render(self) -> RenderResult:
        return '╭─╮\n╰─╯'


class AppTab(Widget):
    def __init__(self, app: App) -> None:
        super().__init__()
        self.os_app = app

    def render(self) -> RenderResult:
        return self.os_app.name


class Taskbar(ScrollableContainer, can_focus=False, can_focus_children=False):
    app: TermOS

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        yield StartButton()

        for app in self.app.os_apps:
            yield AppTab(app)
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
