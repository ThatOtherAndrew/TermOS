from rich.text import Text
from textual.app import RenderResult
from textual.widget import Widget


class MenuBar(Widget):
    def render(self) -> RenderResult:
        return Text(self.app.title, overflow='ellipsis')
