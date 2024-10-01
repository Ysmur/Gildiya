import os
import sqlite3
import sys
import random
import datetime

from PyQt5 import uic
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QApplication, QTableWidget, QHeaderView, QStyleFactory, QWidget, \
    QInputDialog, QMessageBox, QFontDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QColor, QFont, QPixmap


class MyWindowGame(QMainWindow):
    """
    Базовый класс.
    Дизайн
    ------
    main.ui - главное окно приложения

    Атрибуты
    --------

    Основые Методы
    -------

    """

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.score = 0

        self.btn_start.clicked.connect(self.start)
        self.flag_start = True
        self.level = 0
        self.atemp = [1, 2, 3]


        self.tableWidget.itemPressed.connect(self.right_choice)

        self.user = -1
        self.action_new_user_3.triggered.connect(self.open_select_user)

        self.btn_help.clicked.connect(self.show_help)
        self.label.setText('1 этап: Познай мир')
        self.show_help()
        self.action_about.triggered.connect(self.about_program)
        self.selection1 = ['Товар1', 'Товар3', 'Товар6', 'Товар10', 'Товар13']
        self.selection2 = ['Товар2', 'Товар3', 'Товар8', 'Товар11', 'Товар16']
        self.selection3 = ['Товар4', 'Товар8', 'Товар9', 'Товар14', 'Товар15']


    def about_program(self):
        with open('about_program.txt', encoding="utf-8") as f_in:
            data = f_in.read()
        QMessageBox.about(self, 'О программе', data)


    def show_help(self):
        """
        при нажатии на кнопку  помощь открываетсяинструкция по игре
        """
        with open('instruction.txt', encoding='utf-8') as f_in:
            title = [f_in.readline()]
            data = f_in.readlines()

        self.tableWidget.clear()
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.setDisabled(1)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setHorizontalHeaderLabels(title)
        for i in range(4):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(data[i].strip()))
        self.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


    def loadTable_shulte(self, text):
        """
        Размещение товаров на дизайне
        :return:
        """
        n = 4
        with open('blank.txt', encoding="utf-8") as f_in:
            data = f_in.readline().split()
        self.label.setText(f'1 этап: Познай мир. {text}')

        self.fine.hide()
        self.tableWidget.clear()
        self.tableWidget.setShowGrid(True)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setDisabled(0)
        self.tableWidget.setColumnCount(n)
        self.tableWidget.setRowCount(n)
        k = 0
        for i in range(n):
            for j in range(n):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(data[k]))
                self.tableWidget.item(i, j).setTextAlignment(Qt.AlignCenter)

                k += 1
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def right_choice(self):
        """
        Закрашивает правильный выбор зеленым.
        При выборе неправильной буквы, подкрашивает ее на время нажатия красным
        """
        cur_row = self.sender().currentRow()
        cur_col = self.sender().currentColumn()
        cur_num = self.tableWidget.item(cur_row, cur_col).text()
        if self.level == 0:
            self.label.setText('1 этап: Познай мир. 1 раунд: Василий')
            if self.atemp[0] > 0 and cur_num in self.selection1:
                self.selection1.remove(cur_num)
                self.score += 20
                self.time.setText(f'<p style="background: rgb(55, 55, 55); '
                                  f'color: rgb(0, 155, 55)"> {str(self.score)} </p>')
                self.atemp[0] -= 1
                if self.atemp[0] == 0:
                    self.label.setText('1 этап: Познай мир. 2 раунд')
                    self.level += 1
                    print(self.level)
                    self.set_profile(self.level)

                self.tableWidget.item(cur_row, cur_col).setBackground(QColor(200, 250, 210))
            elif self.atemp[0] > 0 and cur_num not in self.selection1:
                self.tableWidget.item(cur_row, cur_col).setBackground(QColor(255, 0, 0))
                self.atemp[0] -= 1
                if self.atemp[0] == 0:
                    self.label.setText('1 этап: Познай мир. 2 раунд')
                    self.level += 1
                    print(self.level)
                    self.set_profile(self.level)
            else:
                self.label.setText('1 этап: Познай мир. 2 раунд')
                self.level += 1
                print(self.level)
                self.set_profile(self.level)
        elif self.level == 1:
            self.label.setText('1 этап: Познай мир. 3 раунд: Евгения')
            if self.atemp[1] and cur_num in self.selection2:
                self.selection2.remove(cur_num)
                self.score += 30
                self.time.setText(f'<p style="background: rgb(55, 55, 55); '
                                  f'color: rgb(0, 155, 55)"> {str(self.score)} </p>')
                self.atemp[0] -= 1
                if self.atemp[0] == 0:
                    self.label.setText('1 этап: Познай мир. 3 раунд')
                    self.level += 1
                    print(self.level)
                    self.set_profile(self.level)

                self.tableWidget.item(cur_row, cur_col).setBackground(QColor(200, 250, 210))
            elif cur_num not in self.selection2:
                self.tableWidget.item(cur_row, cur_col).setBackground(QColor(255, 0, 0))
                self.atemp[1] -= 1
                if self.atemp[0] == 0:
                    self.label.setText('1 этап: Познай мир. 3 раунд')
                    self.level += 1
                    print(self.level)
                    self.set_profile(self.level)
            else:
                self.level += 1
        elif self.level == 2:
            self.label.setText('2 этап: Познай действие')
            if self.atemp[2] and cur_num in self.selection3:
                self.selection3.remove(cur_num)
                self.score += 50
                self.time.setText(f'<p style="background: rgb(55, 55, 55); '
                                  f'color: rgb(0, 155, 55)"> {str(self.score)} </p>')
                self.atemp[2] -= 1
                if self.atemp[0] == 0:
                    self.label.setText('1 этап: Познай действие')
                    self.level += 1
                    print(self.level)
                    self.set_profile(self.level)

                self.tableWidget.item(cur_row, cur_col).setBackground(QColor(200, 250, 210))
            elif cur_num not in self.selection1:
                self.tableWidget.item(cur_row, cur_col).setBackground(QColor(255, 0, 0))
                self.atemp[2] -= 1
                if self.atemp[0] == 0:
                    self.label.setText('1 этап: Познай действие')
                    self.level += 1
                    print(self.level)
                    self.set_profile(self.level)
            else:
                self.level += 1
                self.label.setText('1 этап: Познай действие')
                print(self.level)
                self.set_profile(self.level)
        else:
            #self.sound_no.play()
            self.tableWidget.item(cur_row, cur_col).setBackground(QColor(255, 0, 0))



    def start(self):
        print('start')
        print(self.flag_start, self.user)
        if self.flag_start:
            print('start1')
            #self.btn_start.setText('Стоп')
            self.set_profile(self.level)
            #self.loadTable_shulte()

        else:
             self.btn_start.setText('Старт')
             self.flag_start = True
             #self.table_of_results('fa')

    def set_profile(self, n):
        self.three_form = Profile(n)
        self.three_form.show()
        print('fd')



    def open_select_user(self):
        # открытие окна выбора пользователя
        self.second_form = SelectUser()
        self.second_form.show()

class Profile(QWidget):
    """
    Работа с пользователями
    Дизайн
    ------
    pil.ui - главное окно приложения
    """
    def __init__(self, n):
        super().__init__()
        uic.loadUi('pil.ui', self)
        self.m = n
        with open('consume.txt', encoding="utf-8") as f_in:
            data = f_in.read().split('#')
        #self.label.setText('1 этап: Познай мир. 1 раунд: Василий')
        print(data[self.m])
        data = data[self.m].split('$')
        print(data[0])

        self.pixmap1 = QPixmap('foto/v.png')
        self.pixmap2 = QPixmap('foto/n.png')
        self.pixmap3 = QPixmap('foto/i.png')
        if self.m == 0:
            self.image.setPixmap(self.pixmap1)
        if self.m == 1:
            self.image.setPixmap(self.pixmap2)
        if self.m == 2:
            self.image.setPixmap(self.pixmap3)
        n = 2
        #self.fine.hide()
        self.tableWidget.clear()
        self.tableWidget.setShowGrid(True)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setDisabled(0)
        self.tableWidget.setColumnCount(n-1)
        self.tableWidget.setRowCount(n+1)
        k=1
        for i in range(n - 1):
            for j in range(n + 1):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(data[k]))
                #self.tableWidget.item(i, j).setTextAlignment(Qt.AlignCenter)

                k += 1

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.asc.clicked.connect(self.asc_tovar)

    def asc_tovar(self):
        self.close()
        if self.m == 0:
            ex.loadTable_shulte('1 раунд: Василий')
        if self.m == 1:
            ex.loadTable_shulte('2 раунд: Наталья')
        if self.m == 2:
            ex.loadTable_shulte('3 раунд: Евгения')


    def exit(self):
        """        выход из программы        """
        sys.exit(app.exec())



class SelectUser(QWidget):
    """
    Работа с пользователями
    Дизайн
    ------
    select_user.ui - главное окно приложения
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('select_user.ui', self)
        self.password.setFocus(3)
        self.password.setEchoMode(3)
        self.setWindowModality(Qt.ApplicationModal)
        self.btn_new_user.clicked.connect(self.add_user)
        self.btn_cur_user.clicked.connect(self.current_user)
        self.btn_exit.clicked.connect(self.exit)


        #self.show_name_users()

    def keyPressEvent(self, event):
        """ подтверждение выбора пользователя нажатием на энтер"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.current_user()


    def add_user(self):
        score = 0
        """ добавление в БД информации о новом пользователе """
        name, ok_pressed_1 = QInputDialog.getText(self, "Новая команда",
                                                "Введите название")
        if ok_pressed_1 and name:
            pas, ok_pressed = QInputDialog.getText(self, "Новый пользователь",
                                                      "Введите пароль")

        if ok_pressed:
            with open('names_teams.txt', mode='a', encoding='utf-8') as f:
                print(' '.join([name, pas, str(score)]), file=f)
            ex.user = name
            ex.setWindowTitle(f'Гильдия ИТ-учителей [{name}]')
            self.close()

    def current_user(self):
        """   выбор текущего пользователя    """
        with open('names_teams.txt', mode='r', encoding='utf-8') as f:
            data = f.readlines()
        name = self.name_team.text()
        if name in data:
            ex.user = name
            ex.setWindowTitle(f'Гильдия ИТ-учителей [{name}]')
            print(ex.user)
        self.close()


    def exit(self):
        """        выход из программы        """
        sys.exit(app.exec())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))  # для цветного фона заголовка таблицы результатов
    sys.excepthook = except_hook
    ex = MyWindowGame()
    ex.show()
    sys.exit(app.exec())