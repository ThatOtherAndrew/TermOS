import asyncio

from textual import work
from textual.app import App as TextualApp
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var

from termos.apps import OSApp
from termos.apps.base import tcss_paths
from termos.apps.notepad import Notepad
from termos.components.menu_bar import MenuBar
from termos.components.taskbar import Taskbar
from termos.components.window import Window


class TermOS(TextualApp):
    TITLE = "TermOS"
    CSS_PATH = ["style.tcss", *tcss_paths()]

    windows: var[list[Window]] = var(list)

    def __init__(self):
        super().__init__()
        self.os_apps: list[OSApp] = [Notepad(self)]
        self.windows: list[Window]

    def compose(self) -> ComposeResult:
        yield MenuBar()
        yield Container(classes='desktop')
        yield Taskbar().data_bind(TermOS.windows)

    async def on_mount(self) -> None:
        self.launch_notepad()

    def on_window_created(self, message: Window.Created) -> None:
        self.windows.append(message.window)
        self.mutate_reactive(TermOS.windows)
        message.stop()

    def on_window_closed(self, message: Window.Closed) -> None:
        self.windows.remove(message.window)
        self.mutate_reactive(TermOS.windows)
        message.stop()

    @work
    async def launch_notepad(self) -> None:
        await asyncio.sleep(1)
        self.os_apps[0].launch()
