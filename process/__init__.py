from .ui.main_window import mbAutoRig_window

_main_window = None

def show():
    global _main_window

    if _main_window is not None:
        _main_window.close()
        _main_window.deleteLater()
        
    _main_window = mbAutoRig_window()
    _main_window.show()
    return _main_window