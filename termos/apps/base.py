import abc

from textual.app import ComposeResult
from textual.widget import Widget

from termos.components.window import Window


class OSAppMeta(type(Widget), abc.ABCMeta):
    pass


class OSApp(Widget, abc.ABC, metaclass=OSAppMeta):
    NAME: str
    ICON: str

    @abc.abstractmethod
    def content(self) -> ComposeResult:
        pass

    def compose(self) -> ComposeResult:
        yield Window(self.NAME, self.ICON, self.content())
