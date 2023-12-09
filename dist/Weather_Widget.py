# библиотека для запросов
import requests
import sys
import datetime
import sqlite3

# файл с настройками
from Settings import Settings

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QPixmap
from PIL import Image

er = 0


class MyWidget(QMainWindow, QDialog):
    def __init__(self):
        super().__init__()
        self.weather1 = 0
        self.run()
        global er
        if er == 0:
            self.pushButton_3.clicked.connect(self.update)
            self.pushButton.clicked.connect(self.new_city)
            self.pushButton_2.clicked.connect(self.settings)

    def run(self, a=0):
        self.a = a
        self.city_name = ""
        self.temp = 0
        self.sett = 0

        # ссылки для запросов
        self.http1 = "http://api.openweathermap.org/data/2.5/weather"
        self.http2 = "http://api.openweathermap.org/data/2.5/forecast/"

        # APPID для входа на страницу
        self.appid = 'YOUR_APPID'

        # Подключение базы данных
        con = sqlite3.connect("WeatherDB.db")
        cur = con.cursor()
        result1 = cur.execute("""SELECT Language
                                 FROM Settings
                                 WHERE Condition = 1""").fetchall()
        if result1[0][0] == "RUS":
            result = cur.execute("""SELECT word
                                    FROM Words
                                    WHERE LangId = 1""").fetchall()
        else:
            result = cur.execute("""SELECT word
                                    FROM Words
                                    WHERE LangId = 2""").fetchall()
        con.close()

        if self.a == 0:
            name, ok_pressed = QInputDialog.getText(self, result[22][0],
                                                    result[23][0])
        else:
            name, ok_pressed = QInputDialog.getText(self, result[22][0],
                                                    result[24][0])
        if ok_pressed:
            # запрос с нужными параметрами
            res = requests.get(self.http1,
                               params={"q": self.city_name, 'units': 'metric',
                                       'lang': result[0][0],
                                       'APPID': self.appid}).json()

            if res["cod"] != "404" and name != "":
                self.city_name = name
                uic.loadUi('Weather.ui', self)
                self.setWindowTitle(result[30][0])
                self.show_current_weather()
                self.weather_for_several_days()
            else:
                self.run(1)
        else:
            global er
            er += 1
            self.close()

    def show_current_weather(self):
        self.comboBox.currentTextChanged.connect(self.weather_for_several_days)
        try:
            con = sqlite3.connect("WeatherDB.db")
            cur = con.cursor()
            result2 = cur.execute("""SELECT Language
                                     FROM Settings
                                     WHERE Condition = 1""").fetchall()
            if result2[0][0] == "RUS":
                self.result2 = cur.execute("""SELECT word
                                              FROM Words
                                              WHERE LangId = 1""").fetchall()
            else:
                self.result2 = cur.execute("""SELECT word
                                              FROM Words
                                              WHERE LangId = 2""").fetchall()
            con.close()

            li = [self.result2[13][0], self.result2[14][0]]

            self.setWindowTitle(self.result2[30][0])
            self.label_7.setText(self.result2[12][0])
            self.label_8.setText(self.result2[2][0])
            self.label_9.setText(self.result2[8][0])
            self.label_10.setText(self.result2[1][0])
            self.label_35.setText(self.result2[9][0])
            self.pushButton.setText(self.result2[10][0])
            self.pushButton_2.setText(self.result2[31][0])

            a = self.comboBox.currentText()
            if int(a.split()[0]) == 3:
                self.comboBox.clear()
                self.comboBox.addItem(li[0])
                self.comboBox.addItem(li[1])
            else:
                self.comboBox.clear()
                self.comboBox.addItem(li[1])
                self.comboBox.addItem(li[0])

            # запрос с нужными параметрами
            res = requests.get(self.http1,
                               params={"q": self.city_name, 'units': 'metric',
                                       'lang': self.result2[0][0],
                                       'APPID': self.appid})
            res1 = requests.get(self.http2,
                                params={'q': self.city_name, 'units': 'metric',
                                        'lang': self.result2[0][0],
                                        'APPID': self.appid})

            con = sqlite3.connect("WeatherDB.db")
            cur = con.cursor()
            self.result = cur.execute("""SELECT C_or_F
                                         FROM Settings
                                         WHERE Condition = 1""").fetchall()
            con.close()
            # формат вывода данных
            weather = res.json()
            self.weather1 = res1.json()

            self.label_3.setText(weather['name'].split("’")[0])

            deg = weather["wind"]["deg"]
            if 0 <= deg < 23 or deg >= 337:
                deg = self.result2[3][0]
            elif 23 <= deg < 68:
                deg = self.result2[25][0]
            elif 68 <= deg <= 112:
                deg = self.result2[0][0]
            elif 112 < deg < 157:
                deg = self.result2[26][0]
            elif 157 <= deg <= 202:
                deg = self.result2[4][0]
            elif 202 < deg < 247:
                deg = self.result2[27][0]
            elif 247 <= deg <= 292:
                deg = self.result2[5][0]
            elif 292 < deg < 337:
                deg = self.result2[28][0]

            icon = (weather["weather"][0]["icon"])
            pressure = round(int(weather["main"]['pressure']) * 0.750062)

            if self.result[0][0] == "C":
                self.label.setText(str(round(weather['main']['temp'])) + "°")
            else:
                self.label.setText(str(round(weather['main']['temp'] * 1.8 + 32)) + "°")

            self.label_2.setText(weather['weather'][0]['description'].capitalize())
            self.label_4.setText(str(round(weather["wind"]["speed"], 1)) + self.result2[7][0] + ", " + deg)
            self.label_5.setText(str(weather["main"]["humidity"]) + "%")
            self.label_36.setText(str(pressure) + self.result2[29][0])
            self.lineEdit.setPlaceholderText(self.result2[11][0])

            # изменение размера иконки
            im = Image.open("Icons//" + icon + "@2x" + ".png")
            im2 = im.resize((200, 200))
            im2.save("Icons//" + icon + "@2x" + "1.png")
            self.pixmap = QPixmap("Icons//" + icon + "@2x" + "1.png")
            self.label_37.setPixmap(self.pixmap)

        # исключение ошибок
        except Exception as e:
            print("Exception (weather):", e)
            pass

    def weather_for_several_days(self):
        if self.weather1 != 0 and self.comboBox.currentText() != '':
            s = 0
            a = []
            wind = []
            weekdays1 = []
            icon = []
            c = 0
            dt = 0
            days = [self.label_6, self.label_11, self.label_12, self.label_13, self.label_14]
            wmax = [self.label_15, self.label_16, self.label_17, self.label_18, self.label_19]
            wmin = [self.label_24, self.label_20, self.label_23, self.label_22, self.label_21]
            desc = [self.label_25, self.label_26, self.label_27, self.label_28, self.label_29]
            dayweek = [self.label_30, self.label_31, self.label_32, self.label_33, self.label_34]
            hide = [self.label_13, self.label_14, self.label_18, self.label_19,
                    self.label_22, self.label_21, self.label_28, self.label_29,
                    self.label_33, self.label_34]
            d = []
            week_rus = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            week_eng = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            for i in hide:
                i.hide()

            self.b = self.comboBox.currentText()

            try:
                if self.city_name != "":
                    for f in self.weather1["list"]:
                        if f['dt_txt'].split()[0].split('-')[2] != dt:
                            day = f['dt_txt'].split()[0].split('-')[2]
                            month = f['dt_txt'].split()[0].split('-')[1]
                            year = f['dt_txt'].split()[0].split('-')[0]
                            if day[0] == '0':
                                day = day[1:]
                            if self.result2[0][0] == 'ru':
                                year = int(year)
                                month = int(month)
                                day = int(day)
                                date = week_rus[datetime.date(year=year, month=month, day=day).weekday()]
                                weekdays1.append(str(day) + ', ' + str(date))
                            else:
                                year = int(year)
                                month = int(month)
                                day = int(day)
                                date = week_eng[datetime.date(year=year, month=month, day=day).weekday()]
                                weekdays1.append(str(day) + ', ' + str(date))
                            dt = f['dt_txt'].split()[0].split('-')[2]
                    for i in self.weather1["list"]:
                        if d == []:
                            d.append(i['dt_txt'].split()[0].split('-')[2])
                            if self.result[0][0] == "C":
                                a.append(i["main"]["temp"])
                            else:
                                a.append(i["main"]["temp"] * 1.8 + 32)
                            wind.append(i["wind"]["deg"])
                            icon.append(i["weather"][0]["icon"])
                        elif d != []:
                            if i['dt_txt'].split()[0].split('-')[2] in d:
                                if self.result[0][0] == "C":
                                    a.append(i["main"]["temp"])
                                else:
                                    a.append(i["main"]["temp"] * 1.8 + 32)
                                wind.append(i["wind"]["deg"])
                            else:
                                s += 1

                                wmax[c].setText(str(round(max(a))) + "°")
                                wmin[c].setText(str(round(min(a))) + "°")
                                desc[c].setText(i['weather'][0]['description'].capitalize())
                                wmax[c].show()
                                wmin[c].show()
                                desc[c].show()
                                dayweek[c].setText(weekdays1[c])
                                dayweek[c].show()

                                wind = sum(wind) // len(wind)
                                if 0 <= wind < 23 or wind >= 337:
                                    wind = self.result2[3][0]
                                elif 23 <= wind < 68:
                                    wind = self.result2[25][0]
                                elif 68 <= wind <= 112:
                                    wind = self.result2[0][0]
                                elif 112 < wind < 157:
                                    wind = self.result2[26][0]
                                elif 157 <= wind <= 202:
                                    wind = self.result2[4][0]
                                elif 202 < wind < 247:
                                    wind = self.result2[27][0]
                                elif 247 <= wind <= 292:
                                    wind = self.result2[5][0]
                                elif 292 < wind < 337:
                                    wind = self.result2[28][0]
                                im = Image.open("Icons//" + icon[0][:2] + "d" + "@2x" + ".png")
                                im2 = im.resize((100, 100))
                                im2.save("Icons//" + icon[0] + "@2x" + "1.png")
                                self.pixmap = QPixmap("Icons//" + icon[0] + "@2x" + "1.png")
                                days[c].setPixmap(self.pixmap)
                                days[c].show()
                                icon = []
                                c += 1
                                wind = []
                                a = []
                                d = []
                            if s == int(self.b.split()[0]):
                                break
            # исключение ошибок
            except Exception as e:
                print("Exception (weather):", e)
                pass

    def update(self):
        self.show_current_weather()
        self.weather_for_several_days()
        self.sett = 0

    def new_city(self):
        city = self.lineEdit.text()
        self.city_name = city.capitalize()
        # запрос с нужными параметрами
        res = requests.get(self.http1,
                           params={"q": self.city_name, 'units': 'metric',
                                   'lang': self.result2[0][0],
                                   'APPID': self.appid}).json()

        if res["cod"] != "404" and city != "":
            self.city_name = city
            self.label_38.setText('')
            self.show_current_weather()
            self.weather_for_several_days()
        else:
            self.label_38.setText(self.result2[24][0])

    def settings(self):
        self.set = Settings()
        if self.set.exec_() == 0:
            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.settings()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    if er == 0:
        ex.show()
        sys.exit(app.exec_())
