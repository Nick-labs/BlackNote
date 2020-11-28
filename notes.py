# -*- coding: utf-8 -*-

import sys
import sqlite3

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QStyle, QAction, QMenu, QMessageBox, QApplication
from PyQt5.QtCore import QCoreApplication, QPoint, Qt

from note_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, note=None, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.setFixedSize(220, 260)
        self.settingsButton.setText(u'\u2699')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.textEdit.setStyleSheet('border: 0')
        self.setStyleSheet(f'background-color: {note[4]};')

        self.note = note
        self.textEdit.setText(self.note[1])
        self.move(self.note[2], self.note[3])

        self.menubar_is_active = False

        'Создаем системный трей'
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))

        '''
            Объявляем и добавляем действия для работы с иконкой системного трея
            show - показать окно
            hide - скрыть окно
            close program - выход из программы
        '''

        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        close_action = QAction("Close program", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        close_action.triggered.connect(self.close_program)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(close_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        'Создаем события для menubar'
        exit_action = QAction('&Close note', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close_window)

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        close_program_action = QAction('&Close program', self)
        close_program_action.triggered.connect(self.close_program)

        change_color_white = QAction('White', self)
        change_color_white.triggered.connect(self.change_color)

        change_color_gray = QAction('Gray', self)
        change_color_gray.triggered.connect(self.change_color)

        change_color_red = QAction('Red', self)
        change_color_red.triggered.connect(self.change_color)

        change_color_green = QAction('Green', self)
        change_color_green.triggered.connect(self.change_color)

        change_color_blue = QAction('Blue', self)
        change_color_blue.triggered.connect(self.change_color)

        'Создаем menubar и добавляем в него раннее созданные действия'
        menubar = self.menuBar()
        menubar.hide()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(save_action)
        fileMenu.addAction(exit_action)
        fileMenu.addAction(close_program_action)
        changeColorMenu = fileMenu.addMenu('&Change color')
        changeColorMenu.addAction(change_color_white)
        changeColorMenu.addAction(change_color_gray)
        changeColorMenu.addAction(change_color_red)
        changeColorMenu.addAction(change_color_green)
        changeColorMenu.addAction(change_color_blue)

        self.drag_active = False

        'Коннектим кнопки к определенным событиям'
        self.closeButton.pressed.connect(self.close_window)
        self.settingsButton.pressed.connect(self.menubar_change)
        self.textEdit.textChanged.connect(self.save)

    def change_color(self):
        """Смена цвета заметки"""

        color = self.sender().text()

        if color == 'White':
            color = '#FFFFFF'
        elif color == 'Gray':
            color = '#AAAAAA'
        elif color == 'Red':
            color = '#FF6868'
        elif color == 'Green':
            color = '#A5FF91'
        else:
            color = '#7878CA'

        self.setStyleSheet(f'background-color: {color};')
        cursor.execute(f'''UPDATE notes SET color = "{color}" WHERE id = {self.note[0]}''')

    def save(self):
        """Сохранение заметки в базу данных"""

        cursor.execute(
            f'''UPDATE notes SET text = "{self.textEdit.toPlainText()}",
                x = {self.x()}, y = {self.y()} WHERE id = {self.note[0]}''')
        conn.commit()

    def close_program(self):
        """Завершение программы"""

        QCoreApplication.exit(0)

    def close_window(self):
        """Закрытие(сворачивание) окна"""

        result = QMessageBox.question(self, 'Confirm close', 'Are you sure you want to close the note?')
        if result == QMessageBox.Yes:
            self.close()
            self.save()

    def menubar_change(self):
        """Прячем или показываем menubar"""

        if self.menubar_is_active:
            self.menuBar().hide()
            self.textEdit.setFixedHeight(220)
            self.menubar_is_active = False
        else:
            self.menuBar().show()
            self.textEdit.setFixedHeight(200)
            self.menubar_is_active = True

    """Далее методы для перемещения окна мышкой"""

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
        self.drag_active = True

    def mouseReleaseEvent(self, event):
        if self.drag_active:
            self.save()
            self.drag_active = False


def load_notes():
    """Загружаем заметки из базы данных"""

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    return notes


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    'Подключение к базе данных'
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#AAAAAA'))
    palette.setColor(QPalette.Base, QColor('#AAAAAA'))
    app.setPalette(palette)

    notes = load_notes()

    bn = MainWindow(note=notes[0])
    bn.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

    'Закрытие бахы данных'
    conn.close()
