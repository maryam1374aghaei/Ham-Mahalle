from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>سلام! پروژه هم‌محله با موفقیت اجرا شد 🚀</h1><p>حالا می‌تونی ادامه بدی!</p>")
