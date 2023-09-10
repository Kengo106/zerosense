from django.contrib import admin
from django.urls import path, include
from .views import home_site_view, GradeRaceScraping, GradeRaceResultScraping

urlpatterns = [
    path('', home_site_view, name='base_site'),
    path("getgraderace", GradeRaceScraping.as_view(), name='graderace'),
    path("getgraderaceresult", GradeRaceResultScraping.as_view(),
         name="graderaceresult"),
    path('api/', include('app1.api.urls')),

]
