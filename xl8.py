import configparser
import os
import sys
import darkdetect

from PySide6.QtCore import QDir
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtUiTools import QUiLoader

# clipboard = QApplication.clipboard()
# clipboard.setText("rgb(%d, %d, %d)")

if getattr(sys, 'frozen', False):
   # https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
   APP_PATH = os.path.abspath(os.path.join(sys._MEIPASS, "../Resources"))
else:
   APP_PATH = os.path.dirname(os.path.abspath(__file__))

cfg = configparser.ConfigParser()
cfg.read(os.path.join(APP_PATH, 'config.ini'))
APP_VERSION = cfg['xl8']['APP_VERSION']

ABOUT = \
f"""
<b>
  X-Ray Lima 8
</b>
<p>
Version {APP_VERSION}
<p>
Convert text into Military Alphabet codes
<p>
Neil Okamoto
<br>
<a href=https://github.com/gonewest818/xl8>https://github.com/gonewest818/xl8</a>
"""

def about():
    QMessageBox.about(None, "About X-Ray Lima 8", ABOUT)

def svg_icon(svg):
    # inspired by https://stackoverflow.com/questions/15123544/change-the-color-of-an-svg-in-qt
    #
    # In terms of Porter-Duff compositing, this is an "in" operation
    # so that we get a image with the specified color but the alpha is
    # the contour of the svg.
    pixmap = QPixmap(svg)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    color = 'white' if darkdetect.isDark() else 'black'
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)

def make_military(text):
    alpha = {
        'a': 'Alpha ',
        'b': 'Bravo ',
        'c': 'Charlie ',
        'd': 'Delta ',
        'e': 'Echo ',
        'f': 'Foxtrot ',
        'g': 'Golf ',
        'h': 'Hotel ',
        'i': 'India ',
        'j': 'Juliet ',
        'k': 'Kilo ',
        'l': 'Lima ',
        'm': 'Mike ',
        'n': 'November ',
        'o': 'Oscar ',
        'p': 'Papa ',
        'q': 'Quebec ',
        'r': 'Romeo ',
        's': 'Sierra ',
        't': 'Tango ',
        'u': 'Uniform ',
        'v': 'Victor ',
        'w': 'Whiskey ',
        'x': 'X-ray ',
        'y': 'Yankee ',
        'z': 'Zulu ',
        '1': 'One ',
        '2': 'Two ',
        '3': 'Three ',
        '4': 'Four ',
        '5': 'Five ',
        '6': 'Six ',
        '7': 'Seven ',
        '8': 'Eight ',
        '9': 'Niner ',
        '0': 'Zero ',
        ' ': '\n\n'
    }
    converted = []
    for c in text.lower():
        if c in alpha:
            converted.append(alpha[c])
    return ''.join(converted)

def convert_dialog():
    loader = QUiLoader()
    loader.setWorkingDirectory(QDir(APP_PATH))
    dialog = loader.load(os.path.join(APP_PATH, 'xl8_dialog.ui'))

    def translate(text):
        converted = make_military(text)
        dialog.output.setPlainText(converted)

    dialog.input.textChanged.connect(translate)
    return dialog.exec()

def main():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    icon = svg_icon(os.path.join(APP_PATH, "xl8.svg"))
    tray = QSystemTrayIcon()
    tray.setIcon(icon)

    menu = QMenu()

    convert_action = QAction("Convert...")
    convert_action.triggered.connect(convert_dialog)
    menu.addAction(convert_action)

    menu.addSeparator()

    about_action = QAction("About...")
    about_action.triggered.connect(about)
    menu.addAction(about_action)

    quit_action = QAction("Quit")
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.setVisible(True)

    app.exec()


if __name__ == '__main__':
    main()
