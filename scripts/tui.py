import sys
from modules import shared, script_callbacks, errors


def main(demo, app):
    from tui import sd_tui
    try:
        sd_tui.runTUI()    
    except Exception:
        errors.report('***', exc_info=True)
    finally:
        sys.exit()


if shared.cmd_opts.tui:
    script_callbacks.on_app_started(main)
