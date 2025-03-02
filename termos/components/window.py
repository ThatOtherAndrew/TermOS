from __future__ import annotations

from contextlib import suppress
from enum import Enum
from typing import TYPE_CHECKING

from textual import events
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.css.query import NoMatches
from textual.geometry import Offset
from textual.message import Message
from textual.reactive import reactive, Reactive, var
from textual.widget import Widget
from textual.widgets import Label

if TYPE_CHECKING:
    from termos.apps import OSApp


class TitleBarButton(Widget):
    maximised = reactive(False)

    class Type(Enum):
        MINIMISE = '🗕'
        MAXIMISE = '🗖'
        CLOSE = '🗙'

    class Clicked(Message):
        def __init__(self, button_type) -> None:
            super().__init__()
            self.type = button_type

    def __init__(self, button_type: Type, classes: str):
        super().__init__(classes=classes)
        self.type = button_type

    def render(self) -> str:
        if self.type is self.Type.MAXIMISE and self.maximised:
            return '🗗'
        return self.type.value

    def on_click(self):
        self.post_message(self.Clicked(self.type))


class TitleBar(HorizontalGroup):
    title: Reactive[str | None] = reactive(str)
    icon: Reactive[str | None] = reactive(str)

    def __init__(self, title: str | None, icon: str | None) -> None:
        super().__init__()
        self.title = title
        self.icon = icon

    def compose(self) -> ComposeResult:
        if self.icon is not None:
            yield Label(self.icon, classes='window-icon')
        if self.title is not None:
            yield Label(self.title, classes='window-title')
        with HorizontalGroup(classes='window-controls'):
            yield TitleBarButton(TitleBarButton.Type.MINIMISE, classes="window-minimise-button")
            yield TitleBarButton(TitleBarButton.Type.MAXIMISE, classes="window-maximise-button")
            yield TitleBarButton(TitleBarButton.Type.CLOSE, classes="window-close-button")


class Window(Container):
    title: var[str | None] = var(str)
    icon: var[str | None] = var(str)
    minimised = var(bool)
    maximised = var(bool)
    width: var[int | str] = var('auto')
    height: var[int | str] = var('auto')
    offset: var[tuple[int, int]] = var((0, 0))

    class Created(Message):
        def __init__(self, window: Window) -> None:
            super().__init__()
            self.window = window

    class Minimised(Message):
        def __init__(self, window: Window) -> None:
            super().__init__()
            self.window = window

    class Maximised(Message):
        def __init__(self, window: Window) -> None:
            super().__init__()
            self.window = window

    class Restored(Message):
        def __init__(self, window: Window) -> None:
            super().__init__()
            self.window = window

    class Closed(Message):
        def __init__(self, window: Window) -> None:
            super().__init__()
            self.window = window

    def __init__(
        self,
        parent_app: OSApp,
        content: Widget,
        classes: str | None = None,
        title: str | None = None,
        icon: str | None = None,
        width: int | str = 'auto',
        height: int | str = 'auto',
    ) -> None:
        super().__init__(classes=classes)
        self.mouse_at_drag_start: Offset | None = None
        self.offset_at_drag_start: Offset | None = None
        self.parent_app = parent_app
        self.content = content
        self.title = title
        self.icon = icon
        self.width = width
        self.height = height

    def compose(self) -> ComposeResult:
        yield TitleBar(self.title, self.icon)
        with Container(classes="window-body"):
            yield self.content

    def on_mount(self) -> None:
        self.post_message(Window.Created(self))

    def watch_minimised(self, new: bool) -> None:
        self.styles.display = 'none' if new else 'block'
        self.post_message(self.Minimised(self))

    def watch_maximised(self, new: bool) -> None:
        self.minimised = False
        with suppress(NoMatches):
            self.query_one('.window-maximise-button', TitleBarButton).maximised = new
        if new:
            self.styles.width = '100%'
            self.styles.height = '100%'
            self.styles.offset = (0, 0)
            self.post_message(self.Maximised(self))
        else:
            self.styles.width = self.width
            self.styles.height = self.height
            self.styles.offset = self.offset
            self.post_message(self.Restored(self))

    def watch_width(self, new: int | str) -> None:
        self.maximised = False
        self.styles.width = new

    def watch_height(self, new: int | str) -> None:
        self.maximised = False
        self.styles.height = new

    def watch_offset(self, new: tuple[int, int]) -> None:
        self.maximised = False
        self.styles.offset = new

    def on_title_bar_button_clicked(self, message: TitleBarButton.Clicked):
        if message.type is TitleBarButton.Type.MINIMISE:
            self.minimised = True
        elif message.type is TitleBarButton.Type.MAXIMISE:
            self.maximised = not self.maximised
        elif message.type is TitleBarButton.Type.CLOSE:
            self.post_message(self.Closed(self))

    def on_mouse_down(self, event: events.MouseDown) -> None:
        # self.bring_to_front()

        # continue only on left click
        if event.button != 1:
            return

        # continue only if mouse down on title bar
        widget, _ = self.screen.get_widget_at(*event.screen_offset)
        if widget not in self.query('TitleBar, TitleBar Label'):
            return

        self.focus()
        self.add_class('dragging')

        self.mouse_at_drag_start = event.screen_offset
        self.offset_at_drag_start = Offset(
            int(self.styles.offset.x.value),
            int(self.styles.offset.y.value),
        )
        self.capture_mouse()
        self.can_focus = False

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if (
            self.mouse_at_drag_start is not None
            and self.offset_at_drag_start is not None
        ):
            # adjust window position when snapping out of maximised mode
            if self.maximised:
                x_ratio = event.screen_x / self.screen.size.width
                x_offset = x_ratio * self.width
                self.offset_at_drag_start = Offset(
                    event.screen_x - x_offset,
                    self.offset_at_drag_start.y,
                    )

            self.offset = (
                self.offset_at_drag_start.x + event.screen_x - self.mouse_at_drag_start.x,
                self.offset_at_drag_start.y + event.screen_y - self.mouse_at_drag_start.y,
            )

    def on_mouse_up(self) -> None:
        self.mouse_at_drag_start = None
        self.offset_at_drag_start = None
        self.remove_class('dragging')
        self.release_mouse()
        # self.constrain_to_screen()
        self.can_focus = True
