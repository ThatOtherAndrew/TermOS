from __future__ import annotations

import abc
from importlib import import_module
from pathlib import Path
from typing import Generator, TYPE_CHECKING

from textual.widget import Widget

from termos.components.window import Window

if TYPE_CHECKING:
    from termos.main import TermOS


class OSApp(abc.ABC):
    NAME: str = 'Unnamed App'
    ICON: str = '❓'
    DESCRIPTION: str = ''

    def __init__(self, os: TermOS):
        self.os = os
        self.os.processes.append(self)
        self.os.on_app_launched(self.__class__)

    @staticmethod
    @abc.abstractmethod
    def launch(os: TermOS) -> None:
        pass

    def create_window(
        self,
        content: Widget,
        classes: str | None = None,
        title: str | None | Ellipsis = ...,
        icon: str | None | Ellipsis = ...,
        width: int | str = 'auto',
        height: int | str = 'auto'
    ) -> Window:
        if title is Ellipsis:
            title = self.NAME
        if icon is Ellipsis:
            icon = self.ICON

        window = Window(self, content, classes, title, icon, width, height)
        self.os.query_one('#window-container').mount(window)
        window.focus()
        return window

    async def on_window_close(self, window: Window) -> None:
        await window.remove()
        # Kill the app if it has no remaining windows open
        if not any(window.parent_app is self for window in self.os.windows):
            await self.kill()

    async def kill(self) -> None:
        self.os.processes.remove(self)
        self.os.on_app_killed(self.__class__)


def tcss_paths() -> Generator[str, None, None]:
    for app_dir in Path(__file__).parent.glob('*/*.tcss'):
        app_dir: Path
        if app_dir.is_file():
            yield app_dir.as_posix()


def apps() -> Generator[type[OSApp], None, None]:
    for app_dir in Path(__file__).parent.iterdir():
        app_dir: Path
        if not app_dir.is_dir():
            continue
        init_file = app_dir / '__init__.py'
        if not init_file.is_file():
            continue
        try:
            module = import_module(f'termos.apps.{app_dir.name}.__init__')
        except ImportError:
            continue

        for name in dir(module):
            if name.startswith('_'):
                continue
            obj = getattr(module, name)
            if issubclass(obj, OSApp):
                yield obj
