from django.shortcuts import render
from django.views import View

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from .scraping import initialize_browser, scrape_race_results, GetResult, scrape_data, scrape_grade_race


def home_site_view(request):
    return render(request, 'home.html')


def my_server_route_view(request):
    if request.method == 'POST':
        # ボタンが押されたときの処理を記述する
        browser = initialize_browser()  # ブラウザの初期化
        browser = scrape_race_results(browser)  # レース結果ページまで移動
        GR = GetResult(browser)  # GetResultクラスのインスタンスを作成
        scrape_data(GR, browser)  # データのスクレイピングとDBへの保存
        return render(request, 'finish.html')


class GradeRaceScraping(View):
    def post(self, request):
        browser = initialize_browser()
        scrape_grade_race(browser)
        return render(request, "finish.html")
