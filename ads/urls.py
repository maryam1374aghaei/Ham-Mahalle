from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path('', views.home, name="home"),
    path('create/', views.create_ad, name='create_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
] 


