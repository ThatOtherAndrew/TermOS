from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.message import Message
from textual.reactive import reactive, Reactive
from textual.widget import Widget
from textual.widgets import Label

if TYPE_CHECKING:
    from termos.apps import OSApp


class TitleBarButton(Widget):
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
            yield TitleBarButton(TitleBarButton.Type.MINIMISE, classes="window-minimise")
            yield TitleBarButton(TitleBarButton.Type.MAXIMISE, classes="window-maximise")
            yield TitleBarButton(TitleBarButton.Type.CLOSE, classes="window-close")


class Window(Container):
    title: Reactive[str | None] = reactive(str)
    icon: Reactive[str | None] = reactive(str)

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

    class Closed(Message):
        def __init__(self, window: Window) -> None:
            super().__init__()
            self.window = window

    def __init__(
        self,
        parent_app: OSApp,
        content: ComposeResult,
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
        self.styles.width = width
        self.styles.height = height

    def compose(self) -> ComposeResult:
        yield TitleBar(self.title, self.icon)
        with Container(classes="window-body"):
            yield from self.content

    def on_title_bar_button_clicked(self, message: TitleBarButton.Clicked):
        if message.type is TitleBarButton.Type.MINIMISE:
            ... # TODO
        elif message.type is TitleBarButton.Type.MAXIMISE:
            ... # TODO
        elif message.type is TitleBarButton.Type.CLOSE:
            self.parent_app.close_window(self)
            self.post_message(self.Closed(self))
