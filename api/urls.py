from django.urls import path
from .views import analyze_farm,home

urlpatterns = [
    path("",home, name="home"),
    path("analyze/", analyze_farm, name="analyze_farm"),
]