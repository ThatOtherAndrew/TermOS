import asyncio

from textual import on, work
from textual.app import App as TextualApp
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Header

from termos.apps import OSApp
from termos.apps.base import tcss_paths
from termos.apps.notepad import Notepad
from termos.components.taskbar import Taskbar
from termos.components.window import Window


class TermOS(TextualApp):
    CSS_PATH = ["style.tcss", *tcss_paths()]

    windows = var(list[Window])

    def __init__(self):
        super().__init__()
        self.os_apps: list[OSApp] = [Notepad(self)]
        self.windows = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(classes='desktop')
        yield Taskbar().data_bind(TermOS.windows)

    async def on_mount(self) -> None:
        self.launch_notepad()

    @on(OSApp.WindowCreated)
    def on_window_created(self, message: OSApp.WindowCreated) -> None:
        self.windows.append(message.window)
        self.log(message)
        self.mutate_reactive(TermOS.windows)
        message.stop()

    @work
    async def launch_notepad(self) -> None:
        await asyncio.sleep(1)
        self.os_apps[0].launch()
