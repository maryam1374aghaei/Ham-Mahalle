from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_ad, name='create_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:pk>/edit/', views.edit_ad, name='edit_ad'),
    path('ad/<int:pk>/delete/', views.delete_ad, name='delete_ad'),
    path('my_ads/', views.my_ads, name='my_ads')
    
] 


