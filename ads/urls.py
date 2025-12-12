from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path('', views.home, name="home"),
]
