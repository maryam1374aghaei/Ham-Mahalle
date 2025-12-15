from django.shortcuts import render
from .models import Ad

def home(request):
    ads = Ad.objects.all().order_by('-created_at')  # جدیدترین اول
    context = {
        'ads': ads,
    }
    return render(request, 'ads/home.html', context)