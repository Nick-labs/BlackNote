from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import sqlite3

# Создаем соединение с нашей базой данных
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()


def create_new_note():
    main()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('note.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # self.closeButton.setStyleSheet('''background-color: gray;
        #                                   border-style: outset;
        #                                   border-width: 1px;
        #                                   border-color: gray;
        #                                   font: bold 10px;
        #                                   padding: 6px''')
        self.textEdit.setStyleSheet('border: 0')
        self.load_notes()

        self.closeButton.pressed.connect(self.delete_window)
        # self.newButton.pressed.connect(create_new_note)
        self.textEdit.textChanged.connect(self.save)

    def save(self):
        print(self.textEdit.toPlainText())

    def delete_window(self):
        print('delete')
        result = QMessageBox.question(self, "Confirm delete", "Are you sure you want to delete this note?")
        if result == QMessageBox.Yes:
            self.close()

    # @staticmethod
    def load_notes(self):
        cursor.execute("SELECT * FROM notes")
        notes = cursor.fetchall()
        print(notes)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        if event.button() == Qt.RightButton:
            print('right click')

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

        self.drag_active = True

    def mouseReleaseEvent(self, event):
        if self.drag_active:
            # self.save()
            print('drag')
            self.drag_active = False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#AAAAAA'))
    # palette.setColor(QPalette.WindowText, QColor(121, 85, 72))
    # palette.setColor(QPalette.ButtonText, QColor(121, 85, 72))
    # palette.setColor(QPalette.Text, QColor('#AAAAAA'))
    palette.setColor(QPalette.Base, QColor('#AAAAAA'))
    # palette.setColor(QPalette.AlternateBase, QColor(188, 170, 164))
    app.setPalette(palette)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
    conn.close()


if __name__ == '__main__':
    main()
