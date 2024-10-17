import sys
import UX
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = UX.UX()
    main_menu.showMaximized()
    main_menu.show()
    sys.exit(app.exec_())
