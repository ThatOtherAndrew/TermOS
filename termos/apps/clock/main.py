"""
An App to show the current time.
"""

from datetime import datetime

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Digits

from termos.apps import OSApp
from termos.main import TermOS


class ClockWidget(Widget):
    CSS = """
    Screen { align: center middle; }
    Digits { width: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Digits('')

    def on_mount(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f'{clock:%T}')


class Clock(OSApp):
    NAME = 'Clock'
    ICON = '🕒'
    DESCRIPTION = 'Simple digital clock'

    @staticmethod
    def launch(os: TermOS) -> None:
        Clock(os).create_window(ClockWidget(), width=25, height=4)
