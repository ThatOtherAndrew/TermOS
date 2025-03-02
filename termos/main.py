from textual.app import App as TextualApp
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var

from termos.apps import OSApp
from termos.apps.base import tcss_paths, apps
from termos.components.menu_bar import MenuBar
from termos.components.start_menu import StartMenu
from termos.components.taskbar import Taskbar
from termos.components.window import Window


class TermOS(TextualApp):
    TITLE = "TermOS"
    CSS_PATH = ["style.tcss", *tcss_paths()]
    ALLOW_SELECT = False

    windows: var[list[Window]] = var(list)

    def __init__(self):
        super().__init__()
        self.os_apps: list[type[OSApp]] = [*apps()]
        self.processes: list[OSApp] = []
        self.windows: list[Window]

    def compose(self) -> ComposeResult:
        yield MenuBar()
        yield Container(id='window-container', classes='desktop')
        yield StartMenu()
        yield Taskbar().data_bind(TermOS.windows)

    def on_app_launched(self, app: type[OSApp]) -> None:
        pass

    def on_app_killed(self, app: type[OSApp]) -> None:
        pass

    def on_window_created(self, message: Window.Created) -> None:
        self.windows.append(message.window)
        self.mutate_reactive(TermOS.windows)
        message.stop()

    def on_window_closed(self, message: Window.Closed) -> None:
        self.windows.remove(message.window)
        self.mutate_reactive(TermOS.windows)
        message.window.parent_app.on_window_close(message.window)
        message.stop()
