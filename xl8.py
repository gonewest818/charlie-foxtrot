import darkdetect

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtUiTools import QUiLoader

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

# clipboard = QApplication.clipboard()

# dialog = QColorDialog()

# def copy_color_hex():
#     if dialog.exec():
#         color = dialog.currentColor()
#         clipboard.setText(color.name())

# def copy_color_rgb():
#     if dialog.exec():
#         color = dialog.currentColor()
#         clipboard.setText("rgb(%d, %d, %d)" % (
#             color.red(), color.green(), color.blue()
#         ))

# def copy_color_hsv():
#     if dialog.exec():
#         color = dialog.currentColor()
#         clipboard.setText("hsv(%d, %d, %d)" % (
#             color.hue(), color.saturation(), color.value()
#         ))

def about():
    QMessageBox.about(None, "About X-Ray Lima 8",
"""
<p>X-Ray Lima 8 (v0.1.0)
<br>Convert text into Military Alphabet codes
<p>Neil Okamoto
<br><a href=https://github.com/gonewest818/xl8>https://github.com/gonewest818/xl8</a>
""")


def main():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    icon = svg_icon("xl8.svg")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    menu = QMenu()

    about_action = QAction("About...")
    about_action.triggered.connect(about)
    menu.addAction(about_action)

    convert_action = QAction("Convert...")
    #convert_action.triggered.connect(copy_color_rgb)
    menu.addAction(convert_action)
        
    quit_action = QAction("Quit")
    quit_action.triggered.connect(QApplication.quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)

    app.exec()


if __name__ == '__main__':
    main()
