import os
import sys
if __name__ == "__main__":
    sys.path.append(f"{os.path.dirname(__file__)}{os.sep}..{os.sep}code")
    from controller.init_v_controll_logic.Controller import Controller
    controller = Controller(None, None)
    controller.view.start_view()
