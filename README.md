# TermOS

TermOS is a fantasy operating system and desktop environment which marries the elements of modern UI design language with the retro art of terminal graphics, designed to be as appealing and friendly of an interface as possible to the average modern-day computer user.

TermOS was originally created in 24 hours for [HackLondon 2025](https://www.huzzle.app/events/hacklondon-2025-884200), and won first place for its category of _A World Without X_ (in this case, X being the modern-day graphical user interface).

![TermOS in action](https://i.imgur.com/HU1DP5R.png)

## Features
| Category          | Feature                              | Support | Notes                               |
|-------------------|--------------------------------------|---------|-------------------------------------|
| **Windows**       | Instantiating app windows            | ✅       |                                     |
|                   | Title bars                           | ✅       |                                     |
|                   | Mouse drag-and-drop support          | ✅       |                                     |
|                   | Minimise, maximise and close buttons | ✅       |                                     |
|                   | Window state transitions             | ⚠️      | Dragging maximised windows is buggy |
|                   | Overlapping windows                  | ✅       |                                     |
|                   | Bringing focused window to front     | ✅       |                                     |
|                   | Fade unfocused windows               | ❌       |                                     |
|                   | Window snapping                      | ❌       |                                     |
|                   | Custom window decorations            | ❌       |                                     |
| **Navigation**    | Mouse (point-and-click) support      | ✅       |                                     |
|                   | Keyboard navigation support          | ⚠️      |                                     |
|                   | Window switcher                      | ❌       |                                     |
|                   | Command palette                      | ✅       | Right-click start button            |
| **Interface**     | Taskbar with open windows            | ✅       |                                     |
|                   | Start menu                           | ✅       |                                     |
|                   | Taskbar clock                        | ✅       |                                     |
|                   | Quick settings pane                  | ✅       |                                     |
|                   | Toast notification support           | ✅       |                                     |
| **System**        | Boot screen                          | ❌       |                                     |
|                   | Power off option                     | ✅       |                                     |
|                   | Restart option                       | ⚠️      | Does not reload source code         |
|                   | Automatic system updates             | ❌       |                                     |
|                   | Process management                   | ❌       | Tracks processes internally only    |
| **Customisation** | Preset themes with theme switcher    | ✅       |                                     |
|                   | Persistent settings                  | ❌       |                                     |
| **Applications**  | Applications API                     | ✅       |                                     |
|                   | Pre-installed apps                   | ✅       | Browser, Calculator, Clock, Notepad |
|                   | App store                            | ❌       |                                     |
|                   | Automatic app updates                | ❌       |                                     |
|                   | Hot-reloading apps                   | ❌       |                                     |

## Installation

### uv (recommended)

If you have [uv](https://docs.astral.sh/uv/) installed, you can install TermOS with the following command:

```shell
uv tool install git+https://github.com/ThatOtherAndrew/TermOS
```

You can also run TermOS ephemerally without a permanent installation using `uvx`:

```shell
uvx git+https://github.com/ThatOtherAndrew/TermOS
```

### pip

You can also install TermOS with `pip` (make sure to use `python3` instead of `python` if appropriate on your system):

```shell
python -m pip install git+https://github.com/ThatOtherAndrew/TermOS
```

## Development

To contribute to this project or have a play with the source code, it is strongly recommended to install [uv](https://docs.astral.sh/uv/) first for a consistent development experience. Installation instructions can be found at https://docs.astral.sh/uv/getting-started/installation/.

The below commands will clone this repository and install all dependencies:

```shell
git clone https://github.com/ThatOtherAndrew/TermOS
cd TermOS
uv sync
```

Your cloned instance of TermOS can then be run with the following command:

```shell
uv run termos
```

Alternatively, if you wish to run TermOS in [development mode](https://textual.textualize.io/guide/devtools/#live-editing) for features such as live CSS editing, the following command can be used:

```shell
uv run textual run --dev termos:main
```

For additional features such as [connecting a debug console](https://textual.textualize.io/guide/devtools/#console) or [serving the app in a browser](https://textual.textualize.io/guide/devtools/#serve), please see the relevant [Textual documentation](https://textual.textualize.io/).
