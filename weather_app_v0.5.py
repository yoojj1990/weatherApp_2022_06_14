import sys
import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

form_class = uic.loadUiType('ui/weatherUi.ui')[0]


class WeatherAppWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("오늘의 날씨")
        self.setWindowIcon(QIcon("icons/weather.png"))
        self.statusBar().showMessage('WEATHER APP VER 0.5')

        # 날씨 조회 버튼
        self.weather_button.clicked.connect(self.crawling_weather)

    def crawling_weather(self):

        weather_area = self.input_area.text()  # 유저가 입력한 지역 텍스트 가져오기

        weather_html = requests.get(f"https://search.naver.com/search.naver?&query={weather_area}날씨")

        weather_soup = BeautifulSoup(weather_html.text, 'html.parser')

        try:
            area_text = weather_soup.find('h2', {'class': 'title'}).text  # 검색된 날씨 지역명
            print(area_text)

            today_temper = weather_soup.find('div', {'class': 'temperature_text'}).text  # 현재 온도
            today_temper = today_temper[6:11]
            print(today_temper)

            yesterday_weather = weather_soup.find('p', {'class': 'summary'}).text  # 어제와의 낳씨 비교
            yesterday_weather = yesterday_weather[0:13].strip()  # 13자 까지 가져온후 공백제거 후 저당
            print(yesterday_weather)

            sense_temper = weather_soup.select('dl.summary_list>dd')
            sense_temper_text = sense_temper[0].text  # 체감온도
            print(sense_temper_text)

            today_weather = weather_soup.find('span', {'class': 'weather before_slash'}).text  # 오늘 날씨
            print(today_weather)

            dust_info = weather_soup.select('ul.today_chart_list>li')  # 미세먼지, 초미세먼지 전체 데이터
            # print(dust_info)

            dust1_info = dust_info[0].find('span', {'class': 'txt'}).text  # 미세먼지
            print(dust1_info)

            dust2_info = dust_info[1].find('span', {'class': 'txt'}).text  # 초미세먼지
            print(dust2_info)

            self.area_label.setText(area_text)
            self.setWeatherImage(today_weather)
            self.temper_label.setText(today_temper)
            self.yesterday_label.setText(yesterday_weather)
            self.senseTemper_label.setText(sense_temper_text)
            self.dust1_label.setText(dust1_info)
            self.dust2_label.setText(dust2_info)
        except:
            try:
                area_text = weather_soup.find('span', {'class': 'btn_select'}).text
                area_text = area_text.strip()  # 공백제거
                print(area_text)
                today_temper = weather_soup.find('span', {'class': 'todaytemp'}).text  # 현재온도
                print(today_temper)
                today_weather = weather_soup.find('p', {'class': 'cast_txt'}).text  # 오늘날씨
                today_weather = today_weather[0:2]
                today_weather = today_weather.strip()
                print(today_weather)

                self.area_label.setText(area_text)
                self.setWeatherImage(today_weather)
                self.temper_label.setText(f"{today_temper} ℃")
                self.yesterday_label.setText("-")
                self.senseTemper_label.setText("-")
                self.dust1_label.setText("-")
                self.dust2_label.setText("-")

            except:
                self.area_label.setText("입력된 지역의 날씨 없음")

    # 날씨 정보에 따라 해당 날씨 이미지 출력 함수
    def setWeatherImage(self, weatherInfo):
        if weatherInfo == "흐림":
            weatherImg = QPixmap("img/cloud.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif weatherInfo == "맑음":
            weatherImg = QPixmap("img/sun.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif weatherInfo == "눈":
            weatherImg = QPixmap("img/snow.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif weatherInfo == "비":
            weatherImg = QPixmap("img/rain.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif weatherInfo == "구름많음":
            weatherImg = QPixmap("img/cloud.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        else:
            self.weather_label.setText(weatherInfo)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherAppWindow()
    ex.show()
    sys.exit(app.exec_())
