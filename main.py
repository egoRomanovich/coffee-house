import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class EditWidget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)

        self.buttonBox.accepted.connect(self.execute_query)
        self.buttonBox.rejected.connect(self.reject)

    def execute_query(self):
        query = self.queryEdit.toPlainText().strip()
        if query:
            try:
                con = sqlite3.connect("coffee.sqlite")
                cur = con.cursor()
                cur.execute(query)
                con.commit()
                con.close()
                self.accept()
            except sqlite3.Error as e:
                self.reject()
        else:
            self.reject()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_table()
        self.editButton.clicked.connect(self.edit_table)

    def load_table(self):
        self.tableWidget.verticalHeader().setVisible(False)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute('SELECT * FROM Coffees').fetchall()
        title = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена',
                 'Объем упаковки (мл)']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def edit_table(self):
        ew = EditWidget()
        if ew.exec() == QDialog.DialogCode.Accepted:
            self.statusBar().showMessage("Запрос выполнен успешно.")
            self.load_table()
        else:
            self.statusBar().showMessage("Запрос не был выполнен.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())