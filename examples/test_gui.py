# wl-19-09-2024, Thu: debug GUI functions

import sys
from PySide6.QtWidgets import QApplication
import lamp_gui as gui


def main():
    # Exception Handling
    try:
        app = QApplication(sys.argv)
        form = gui.lamp_app()
        form.show()
        # sys.exit(app.exec())
        app.exec()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])


if __name__ == '__main__':
    main()
