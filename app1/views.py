from django.shortcuts import render
from django.views import View

# Create your views here.
from django.shortcuts import render

from .scraping import initialize_browser, scrape_grade_race, scrape_grade_race_result


def home_site_view(request):
    return render(request, 'home.html')


class GradeRaceScraping(View):
    def post(self, request):
        browser = initialize_browser()
        scrape_grade_race(browser)
        return render(request, "finish.html")


class GradeRaceResultScraping(View):
    def post(self, request):
        browser = initialize_browser()
        scrape_grade_race_result(browser)
        return render(request, "finish.html")
