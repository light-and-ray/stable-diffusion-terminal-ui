from __future__ import annotations
import pytermgui as ptg


PALETTE_LIGHT = "#1b0dd6"
PALETTE_MID = "#1b0dd6"
PALETTE_DARK = "#42404d"
PALETTE_DARKER = "#242321"


def create_aliases() -> None:

    ptg.tim.alias("app.text", "#cfc7b0")

    ptg.tim.alias("app.header", f"bold @{PALETTE_MID} #d9d2bd")
    ptg.tim.alias("app.header.fill", f"@{PALETTE_LIGHT}")

    ptg.tim.alias("app.title", f"bold {PALETTE_LIGHT}")
    ptg.tim.alias("app.button.label", f"bold @{PALETTE_DARK} app.text")
    ptg.tim.alias("app.button.highlight", "inverse app.button.label")

    ptg.tim.alias("app.footer", f"@{PALETTE_DARKER}")


def configure_widgets() -> None:

    ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
    ptg.boxes.ROUNDED.set_chars_of(ptg.Container)

    ptg.Button.styles.label = "app.button.label"
    ptg.Button.styles.highlight = "app.button.highlight"

    ptg.Slider.styles.filled__cursor = PALETTE_MID
    ptg.Slider.styles.filled_selected = PALETTE_LIGHT

    ptg.Label.styles.value = "app.text"

    ptg.Window.styles.border__corner = "#C2B280"
    ptg.Container.styles.border__corner = PALETTE_DARK

    ptg.Splitter.set_char("separator", "")


def define_layout() -> ptg.Layout:

    layout = ptg.Layout()

    # A header slot with a height of 1
    layout.add_slot("Header", height=1, width=1.0)
    layout.add_break()

    layout.add_slot("Body")

    layout.add_slot("Body right", width=0.5)

    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("Footer", height=1)

    return layout
