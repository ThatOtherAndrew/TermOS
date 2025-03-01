from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.reactive import reactive, Reactive
from textual.widget import Widget
from textual.widgets import Label

if TYPE_CHECKING:
    from termos.apps import OSApp


class TitleBarButton(Widget):
    def __init__(self, symbol: str, classes: str):
        super().__init__(classes=classes)
        self.symbol = symbol

    def render(self) -> str:
        return self.symbol


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
            yield TitleBarButton("🗕", classes="window-minimise")
            yield TitleBarButton("🗖", classes="window-maximise")
            yield TitleBarButton("🗙", classes="window-close")


class Window(Container):
    title: Reactive[str | None] = reactive(str)
    icon: Reactive[str | None] = reactive(str)

    def __init__(
        self,
        parent_app: OSApp,
        content: ComposeResult,
        title: str | None = None,
        icon: str | None = None,
        width: int | str = 'auto',
        height: int | str = 'auto',
    ) -> None:
        super().__init__()
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
