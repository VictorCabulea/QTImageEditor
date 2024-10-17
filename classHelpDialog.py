from PyQt5.QtWidgets import QVBoxLayout, QDialog, QTextBrowser


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super(CustomDialog, self).__init__(parent)
        self.setWindowTitle("Help")

        layout = QVBoxLayout(self)

        text_browser = QTextBrowser(self)
        layout.addWidget(text_browser)

        try:
            with open("Resurse/Help/help.txt", "r", encoding="utf-8") as file:
                help_text = file.read()

            if help_text:
                text_browser.setPlainText(help_text)
            else:
                text_browser.setPlainText("Unable to load help text from file.")
        except FileNotFoundError:
            text_browser.setPlainText("The help file (help.txt) was not found.")
        except Exception as e:
            text_browser.setPlainText(f"An error occurred while reading the help file: {str(e)}")

        self.setGeometry(100, 100, 800, 400)
