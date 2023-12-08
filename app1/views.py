from django.shortcuts import render
from django.views import View
from .models import Race
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
import pytz
from django.conf import settings
import os
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


class FinishVoteView(View):
    def post(self, request):
        utc_now = timezone.now()
        jst = pytz.timezone('Asia/Tokyo')
        jst_now = utc_now.astimezone(jst)
        now_date = jst_now.date()
        print(jst_now, now_date)
        vote_deadline_plusone = (jst_now + timedelta(hours=1)).time()
        races = Race.objects.filter(
            Q(race_date=now_date) &
            Q(start_time__lte=vote_deadline_plusone)
        )
        for race in races:
            race.is_votable = 2
            race.save()
        return render(request, 'finish.html')


class MainAppView(View):
    def get(self, request):
        return render(request, 'index.html')
