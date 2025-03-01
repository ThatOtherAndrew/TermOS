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

    class WindowCreated(Message):
        def __init__(self, window: Window) -> None:
            super().__init__()
            self.window = window

    def __init__(self, os: TermOS):
        self.os = os

    @abc.abstractmethod
    def launch(self) -> None:
        pass

    def create_window(
        self,
        content: ComposeResult,
        title: str = NAME,
        icon: str = ICON,
        width: int | str = 'auto',
        height: int | str = 'auto'
    ) -> Window:
        window = Window(self, content, title, icon, width, height)
        self.os.query_one('.desktop').mount(window)
        window.post_message(self.WindowCreated(window))
        return window


def tcss_paths() -> Generator[str, Any, None]:
    for app_dir in Path(__file__).parent.glob('*/*.tcss'):
        app_dir: Path
        if app_dir.is_file():
            yield app_dir.as_posix()
