from __future__ import annotations

from contextlib import suppress
from enum import Enum
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.css.query import NoMatches
from textual.message import Message
from textual.reactive import reactive, Reactive
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
    title: Reactive[str | None] = reactive(str)
    icon: Reactive[str | None] = reactive(str)
    minimised = reactive(bool)
    maximised = reactive(bool)
    width: Reactive[int | str] = reactive('auto')
    height: Reactive[int | str] = reactive('auto')

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
            self.post_message(self.Maximised(self))
        else:
            self.styles.width = self.width
            self.styles.height = self.height
            self.post_message(self.Restored(self))

    def watch_width(self, new: int | str) -> None:
        self.maximised = False
        self.styles.width = new

    def watch_height(self, new: int | str) -> None:
        self.maximised = False
        self.styles.height = new

    def on_title_bar_button_clicked(self, message: TitleBarButton.Clicked):
        if message.type is TitleBarButton.Type.MINIMISE:
            self.minimised = True
        elif message.type is TitleBarButton.Type.MAXIMISE:
            self.maximised = not self.maximised
        elif message.type is TitleBarButton.Type.CLOSE:
            self.parent_app.close_window(self)
            self.post_message(self.Closed(self))
