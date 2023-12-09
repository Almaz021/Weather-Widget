import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect("WeatherDB.db")
        cur = con.cursor()
        result = cur.execute("""SELECT C_or_F
                                FROM Settings
                                WHERE Condition = 1""").fetchall()
        result1 = cur.execute("""SELECT Language
                                 FROM Settings
                                 WHERE Condition = 1""").fetchall()

        if result1[0][0] == "RUS":
            self.result = cur.execute("""SELECT word
                                             FROM Words
                                             WHERE LangId = 1""").fetchall()
        else:
            self.result = cur.execute("""SELECT word
                                         FROM Words
                                         WHERE LangId = 2""").fetchall()
        con.close()

        uic.loadUi('Settings.ui', self)

        self.setWindowTitle(self.result[31][0])
        self.label.setText(self.result[16][0])
        self.label_2.setText(self.result[17][0])
        self.pushButton.setText(self.result[18][0])
        self.pushButton_2.setText(self.result[19][0])
        self.radioButton_3.setText(self.result[20][0])
        self.radioButton_4.setText(self.result[21][0])

        if result[0][0] == "C":
            self.radioButton_3.setChecked(True)
        else:
            self.radioButton_4.setChecked(True)

        if result1[0][0] == "RUS":
            self.radioButton.setChecked(True)
        else:
            self.radioButton_2.setChecked(True)

        self.pushButton_2.clicked.connect(self.cancel)
        self.pushButton.clicked.connect(self.ok)
        self.show()

    def cancel(self):
        self.close()

    def ok(self):
        con = sqlite3.connect("WeatherDB.db")
        cur = con.cursor()
        if self.radioButton.isChecked():
            result = cur.execute("""UPDATE Settings
                                    SET Condition = 1
                                    WHERE Language = 'RUS'""").fetchall()
            con.commit()
            result = cur.execute("""UPDATE Settings
                                    SET Condition = 0
                                    WHERE Language = 'ENG'""").fetchall()
            con.commit()
        elif self.radioButton_2.isChecked():
            result = cur.execute("""UPDATE Settings
                                    SET Condition = 0
                                    WHERE Language = 'RUS'""").fetchall()
            con.commit()
            result = cur.execute("""UPDATE Settings
                                    SET Condition = 1
                                    WHERE Language = 'ENG'""").fetchall()
            con.commit()
        if self.radioButton_3.isChecked():
            result = cur.execute("""UPDATE Settings
                                    SET C_or_F = 'C'
                                    WHERE C_or_F = 'F'""").fetchall()
            con.commit()
        elif self.radioButton_4.isChecked():
            result = cur.execute("""UPDATE Settings
                                    SET C_or_F = 'F'
                                    WHERE C_or_F = 'C'""").fetchall()
            con.commit()
        con.close()

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Settings()
    ex.show()
    sys.exit(app.exec_())
