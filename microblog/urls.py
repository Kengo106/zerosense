
from django.contrib import admin
from django.urls import path

from blog.views import frontpage,post_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path("<slug:slug>/", post_detail, name="post_detail"),  # 初めのslugでurlからの値を受け取りそれを後ろのslugに渡し、views.pyのpost_detailに渡すname=でこのurlに名前を付ける
    path("", frontpage),

]
