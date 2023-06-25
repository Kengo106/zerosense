from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from .scraping import initialize_browser, scrape_race_results, GetResult, scrape_data

def home_site_view(request):
    return render(request, 'home.html')

def my_server_route_view(request):
    if request.method == 'POST':
        # ボタンが押されたときの処理を記述する
        browser = initialize_browser()  # ブラウザの初期化
        browser = scrape_race_results(browser)  # レース結果ページまで移動
        GR = GetResult(browser)  # GetResultクラスのインスタンスを作成
        scrape_data(GR, browser)  # データのスクレイピングとDBへの保存
        return HttpResponse("スクレイピングを実行しました！")

    return render(request, 'templates/base.html')
