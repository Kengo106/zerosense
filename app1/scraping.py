from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as  pd
from django.db import transaction
from .models import RaceResult, Odds
import os
import time

# scraping.pyのディレクトリを取得



def initialize_browser():
    # Chrome WebDriverのパスを指定
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # WebDriverのパスを指定
    webdriver_path = os.path.join(script_dir, "chromedriver.exe")

    # Chromeのヘッドレスオプションを設定する
    #chrome_options = Options()
    #chrome_options.add_argument('--headless')

    # Serviceオブジェクトを作成
    service = Service(webdriver_path)

    # Chromeを起動
    #browser = webdriver.Chrome(service=service, options=chrome_options)
    browser = webdriver.Chrome(service=service)

    return browser



#  スクレイピングしたいページまで移動
def scrape_race_results(browser):

    # 起動したWebDriverにJRAのURLを入力
    url = "https://www.jra.go.jp/"
    browser.get(url)

    elem_quick_menu = browser.find_element(By.ID, "quick_menu")  # 上のクイックメニューを選択
    elem_quick_menu_list = elem_quick_menu.find_elements(By.TAG_NAME, "li")  # クイックメニューからレース結果を指定するためにliタグを指定
    elem_race = elem_quick_menu_list[3]  # 左から4項目目のレース結果を選択

    elem_race.click()
    time.sleep(1)  # 5秒間プログラムを一時停止


    # browser.find_element(By.CLASS_NAME, "link_list multi div3 center")
    race_list = browser.find_element(By.ID, "main")
    race_list = race_list.find_elements(By.CLASS_NAME, "link_list")  # レース結果の表を取得

    if race_list:
        race_list = race_list[0].find_elements(By.TAG_NAME, "div")  # レース結果の上段を取得
        race_page = race_list[0]  # レース結果の上段左を取得
    else:  # レース結果がまだ出ていないとき(週末)
        race_list = browser.find_elements(By.CLASS_NAME, "cell.kaisai")[0]
        race_page = race_list.find_elements(By.TAG_NAME, "a")[0]

    race_page.click()
    time.sleep(1) 

    race_page_list = browser.find_elements(By.CLASS_NAME, "race_num")  # レース結果の1R,2R,,,,を取得
    R1_race_page = race_page_list[1]  # R1レース結果を取得
    R1_race_page.click()
    time.sleep(1)   # R1レース結果まで移動

    return browser



class GetResult:
    
    def __init__(self, browser):
        self.soup = BeautifulSoup(browser.page_source, "html.parser")
        race_list = browser.find_elements(By.CSS_SELECTOR, "ul.nav.race-num.mt15")[0]
        self.race_list = race_list.find_elements(By.TAG_NAME, "li")
        self.day_location_list = browser.find_elements(By.CSS_SELECTOR, "div.link_list.multi.div3.center.mid.narrow")
        self.num_locations = len(self.day_location_list[0].find_elements(By.TAG_NAME, "div"))
        self.num_days = len(self.day_location_list)
        self.num_races = len(self.race_list)
        self.browser = browser

    def get_page(self):  # ページ情報の取得
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")
        race_list = self.browser.find_elements(By.CSS_SELECTOR, "ul.nav.race-num.mt15")[0]
        self.race_list = race_list.find_elements(By.TAG_NAME, "li")
        self.day_location_list = self.browser.find_elements(By.CSS_SELECTOR, "div.link_list.multi.div3.center.mid.narrow")
        self.num_locations = len(self.day_location_list[0].find_elements(By.TAG_NAME, "div"))
        self.num_days = len(self.day_location_list)
        self.num_races = len(self.race_list)
        
    def move_select_race(self, race):  # レース番号の指定
        self.get_page()
        self.race_list[race].click()
        self.get_page()
        
    def move_select_day_location(self, day, location):  # 開催日と開催場所を指定
        self.get_page()
        self.day_location_list[day].find_elements(By.TAG_NAME, "div")[location].click()
        self.get_page()
        

    def get_result(self):  # レース結果の取得
        self.get_page()
        for btn in self.browser.find_elements(By.CSS_SELECTOR, "a.btn-def.btn-sm.blue.btn-block"):
            if btn.text == 'レース結果':
                btn.click()
            else:
                pass
            
        self.get_page()

        tables = self.soup.tbody
        tables = tables.find_all("tr")
        
        self.result = []

        for table in tables:
            num_list = table.find_all("td", attrs={"class": "num"})
            try:  # エラーが発生する可能性のあるコード (要検討)
                num_num = int(num_list[0].text)
            except:  # エラー発生時の処理
                num_num = None

            place_list = table.find_all("td", attrs={"class": "place"})
            try:
                place_num = int(place_list[0].text)
            except:
                place_num = None

            weight_list = table.find_all("td", attrs={"class": "weight"})
            try:
                weight_num = float(weight_list[0].text)
            except:
                weight_num = None

            h_weight_list = table.find_all("td", attrs={"class": "h_weight"})
            try:
                h_weight_num = int(str(h_weight_list[0].text).split("(")[0])
            except:
                h_weight_num = None


            pop_list = table.find_all("td", attrs={"class": "pop"})
            try:
                pop_num = int(pop_list[0].text)
            except:
                pop_num = None            


            time_list = table.find_all("td", attrs={"class": "time"})
            time_str = str(time_list[0].text)

            horse_list = table.find_all("td", attrs={"class": "horse"})
            horse_str = str(horse_list[0].text).replace("\n","")

            trainer_list = table.find_all("td", attrs={"class": "trainer"})
            trainer_str = str(trainer_list[0].text).replace("\n","")

            jockey_list = table.find_all("td", attrs={"class": "jockey"})
            jockey_str = str(jockey_list[0].text).replace("\n","")

            result_datum = {}
            result_datum["馬番"] = num_num
            result_datum["着順"] = place_num
            result_datum["馬名"] = horse_str
            result_datum["負担重量"] = weight_num
            result_datum["騎手名"] = jockey_str
            result_datum["調教師名"] = trainer_str
            result_datum["タイム"] = time_str
            result_datum["馬体重"] = h_weight_num
            result_datum["人気"] = pop_num
            result_datum["レース名"] = self.soup.find("span", attrs = {"class": "opt"}).text
            self.result.append(result_datum)
            
        return self.result
          
    def get_odds(self):  # 最終オッズの取得
        self.get_page()
        for btn in self.browser.find_elements(By.CSS_SELECTOR, "a.btn-def.btn-sm.blue.btn-block"):
            if btn.text == 'オッズ':
                btn.click()
            else:
                pass
        
        self.get_page()
        
        tables = self.soup.tbody
        tables = tables.find_all("tr")
        
        
        
        self.odds = []

        for table in tables:
            num_list = table.find_all("td", attrs={"class": "num"})
            try:  # エラーが発生する可能性のあるコード
                num_num = int(num_list[0].text)
            except:  # エラー発生時の処理
                num_num = None
                
            odds_tan_list = table.find_all("td", attrs={"class": "odds_tan"})
            try:
                odds_tan_num = float(odds_tan_list[0].text)
            except:
                odds_tan_num = None

            odds_fuku_list = table.find_all("td", attrs={"class": "odds_fuku"})
           
            if odds_fuku_list[0].text == "取消":
                    odds_fuku_min_num = -1
                    odds_fuku_max_num = -1

            else:
                try:
                    odds_fuku_min_num = float(odds_fuku_list[0].find_all("span", attrs={"class": "min"})[0].text)
                except:
                    odds_fuku_min_num = None

                try:
                    odds_fuku_max_num = float(odds_fuku_list[0].find_all("span", attrs={"class": "max"})[0].text)
                except:
                    odds_fuku_max_num = None
                
            horse_list = table.find_all("td", attrs={"class": "horse"})
            horse_str = str(horse_list[0].text).replace("\n","")

            odds_datum = {}
            odds_datum["馬番"] = num_num
            odds_datum["単勝"] = odds_tan_num
            odds_datum["複勝最小"] = odds_fuku_min_num
            odds_datum["複勝最大"] = odds_fuku_max_num
            odds_datum["馬名"] =  horse_str
            odds_datum["レース名"] = self.soup.find("span", attrs = {"class": "opt"}).text

            self.odds.append(odds_datum)
            
        return self.odds
    
    def save_to_db(self):
        with transaction.atomic():
            for result_data in self.result:
                RaceResult.objects.update_or_create(
                    horse_number=result_data['馬番'],
                    race_name=result_data['レース名'],
                    defaults={
                        'horse_name': result_data['馬名'],
                        'place_num': result_data['着順'],
                        'jockey_name': result_data['騎手名'],
                        'trainer_name': result_data['調教師名'],
                        'time': result_data['タイム'],
                        'h_weight': result_data['馬体重'],
                        'pop': result_data['人気'],
                    }
                )

            for odds_data in self.odds:
                Odds.objects.update_or_create(
                    horse_number=odds_data['馬番'],
                    race_name=odds_data['レース名'],
                    defaults={
                        'horse_name': odds_data['馬名'],
                        'odds_tan': odds_data['単勝'],
                        'odds_fuku_min': odds_data['複勝最小'],
                        'odds_fuku_max': odds_data['複勝最大'],
                    }
                )
                

def scrape_data(GR, browser):
    for day in range(GR.num_days):
        for location in range(GR.num_locations):
            GR.move_select_day_location(day,location)  # 開催日と開催場所を指定
            for race in range(GR.num_races):    
                GR.move_select_race(race)  # レース番号を指定
                GR.get_result()  # レース結果を取得
                GR.get_odds()  # オッズを取得
                GR.save_to_db()  # dbに保存

    return browser.quit() # ブラウザを閉じる
  