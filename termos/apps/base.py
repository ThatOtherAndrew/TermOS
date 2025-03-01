import abc
from pathlib import Path
from typing import Any, Generator

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


def tcss_paths() -> Generator[str, Any, None]:
    for app_dir in Path(__file__).parent.glob('*/*.tcss'):
        app_dir: Path
        if app_dir.is_file():
            yield app_dir.as_posix()
