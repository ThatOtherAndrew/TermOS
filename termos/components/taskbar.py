from textual import events, widgets
from textual.app import ComposeResult, RenderResult
from textual.containers import ScrollableContainer
from textual.widget import Widget

from termos.apps import App


class TaskbarApp(Widget):
    # language=SCSS
    DEFAULT_CSS = """
    TaskbarApp {
        width: auto;
        height: auto;
        border: round;
    }
    """

    def __init__(self, app: App) -> None:
        super().__init__()
        self.os_app = app

    def render(self) -> RenderResult:
        return self.os_app.name


class Taskbar(ScrollableContainer, can_focus=False, can_focus_children=False):
    ALLOW_SELECT = False
    # language=SCSS
    DEFAULT_CSS = """
    Taskbar {
        layout: horizontal;
        width: 100%;
        height: 3;
        dock: bottom;
        scrollbar-size: 0 0;
        color: $footer-foreground;
        background: $footer-background;
    }
    """

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        for app in self.app.os_apps:
            yield TaskbarApp(app)

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
