from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
from markdownify import markdownify
from textual import work
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widget import Widget
from textual.widgets import MarkdownViewer, Input, Button

from termos.apps import OSApp

if TYPE_CHECKING:
    from termos.main import TermOS


class BrowserWidget(Widget):
    def __init__(self, session: httpx.AsyncClient) -> None:
        super().__init__()
        self.session = session

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Button('Toggle sidebar', variant='primary')
            yield Input(placeholder='https://example.com', classes='url-input')
        yield MarkdownViewer(open_links=False)

    def on_input_submitted(self, message: Input.Submitted) -> None:
        self.fetch_web_page(message.value)

    @work(exclusive=True, exit_on_error=False)
    async def fetch_web_page(self, url: str) -> None:
        response = await self.session.get(url)
        markdown = markdownify(response.text)
        await self.query_one(MarkdownViewer).document.update(markdown)

    def on_button_pressed(self) -> None:
        viewer = self.query_one(MarkdownViewer)
        viewer.show_table_of_contents = not viewer.show_table_of_contents


class Browser(OSApp):
    NAME = 'Browser'
    ICON = '🌐'
    DESCRIPTION = 'Read web pages using Markdown'

    def __init__(self, os: TermOS) -> None:
        super().__init__(os)
        self.client = httpx.AsyncClient(follow_redirects=True)

    async def kill(self) -> None:
        await self.client.aclose()
        await super().kill()

    @staticmethod
    def launch(os: TermOS) -> None:
        instance = Browser(os)
        instance.create_window(BrowserWidget(instance.client), 'browser', width=150, height=40)
