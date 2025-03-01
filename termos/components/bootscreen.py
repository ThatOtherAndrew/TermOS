from textual.widget import Widget
from textual.widgets import Static
import asyncio


class BootScreen(Widget):
# A static boot screen that shows the TermOS logo.

    def compose(self):
        """Displays the OS logo."""
        logo = """
████████╗███████╗██████╗ ███╗   ███╗ ██████╗ ███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔═══██╗██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║███████╗
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║╚════██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝███████║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝
        Welcome to TermOS - Your Terminal OS!
        """
        yield Static(logo, classes="boot-logo")

    async def on_mount(self):
        """Remove the boot screen after a delay."""
        await asyncio.sleep(2)
        await self.remove()
