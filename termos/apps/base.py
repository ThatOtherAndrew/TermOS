from __future__ import annotations

import abc
from pathlib import Path
from typing import Any, Generator, TYPE_CHECKING

from textual.app import ComposeResult
from textual.message import Message

from termos.components.window import Window

if TYPE_CHECKING:
    from termos.main import TermOS


class OSApp(abc.ABC):
    NAME: str = 'Unnamed App'
    ICON: str = '❓'
    DESCRIPTION: str = ''

    def __init__(self, os: TermOS):
        self.os = os

    @abc.abstractmethod
    def launch(self) -> None:
        pass

    def create_window(
        self,
        content: ComposeResult,
        title: str | None | Ellipsis = ...,
        icon: str | None | Ellipsis = ...,
        width: int | str = 'auto',
        height: int | str = 'auto'
    ) -> Window:
        if title is Ellipsis:
            title = self.NAME
        if icon is Ellipsis:
            icon = self.ICON

        window = Window(self, content, title, icon, width, height)
        self.os.query_one('.desktop').mount(window)
        window.post_message(Window.Created(window))
        return window

    # noinspection PyMethodMayBeStatic
    def close_window(self, window: Window) -> None:
        window.remove()


def tcss_paths() -> Generator[str, Any, None]:
    for app_dir in Path(__file__).parent.glob('*/*.tcss'):
        app_dir: Path
        if app_dir.is_file():
            yield app_dir.as_posix()
