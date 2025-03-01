from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label


class TitleBarButton(Widget):
    def __init__(self, symbol: str, classes: str):
        super().__init__(classes=classes)
        self.symbol = symbol

    def render(self) -> str:
        return self.symbol


class TitleBar(HorizontalGroup):
    title = reactive(str)
    icon = reactive(str)

    def __init__(self, title: str, icon: str) -> None:
        super().__init__()
        self.title = title
        self.icon = icon

    def compose(self) -> ComposeResult:
        yield Label(self.icon)
        yield Label(self.title)
        with HorizontalGroup():
            yield TitleBarButton("🗕", classes="window-minimise")
            yield TitleBarButton("🗖", classes="window-maximise")
            yield TitleBarButton("🗙", classes="window-close")


class Window(Container):
    def __init__(self, title: str, icon: str, content: ComposeResult) -> None:
        super().__init__()
        self.title_bar = TitleBar(title, icon)
        self.content = content

    def compose(self) -> ComposeResult:
        yield self.title_bar
        yield from self.content
