from __future__ import annotations
import signal
import pytermgui as ptg
from modules import shared
from tui.from_gradio import makeColumn, findElementById
from tui.config import create_aliases, configure_widgets, define_layout



def confirm_quit(manager: ptg.WindowManager) -> None:
    """Creates an "Are you sure you want to quit" modal window"""

    modal = ptg.Window(
        "[app.title]Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)




def runTUI() -> None:
    """Runs the application."""

    create_aliases()
    configure_widgets()


    with ptg.WindowManager() as manager:
        signal.signal(signal.SIGINT, lambda *args: manager.stop())
        manager.layout = define_layout()

        header = ptg.Window(
            "[app.header] Welcome to PyTermGUI ",
            box="EMPTY",
            is_persistant=True,
        )

        header.styles.fill = "app.header.fill"

        # Since header is the first defined slot, this will assign to the correct place
        manager.add(header)

        footer = ptg.Window(
            ptg.Button("Quit", lambda *_: confirm_quit(manager)),
            box="EMPTY",
        )
        footer.styles.fill = "app.footer"

        # Since the second slot, body was not assigned to, we need to manually assign
        # to "footer"
        manager.add(footer, assign="footer")

        manager.add(
            ptg.Window("My sidebar"),
            assign="body_right",
        )

        manager.add(
            ptg.Window(
                makeColumn(findElementById(shared.demo, 'txt2img_settings')),
                vertical_align=ptg.VerticalAlignment.TOP,
                overflow=ptg.Overflow.SCROLL,
            ),
            assign="body",
        )
