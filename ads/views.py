from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ad, Category, AdImage
import django.db.models as models


def home(request):
    ads = Ad.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    # گرفتن پارامترهای جستجو و فیلتر از GET
    
    search_query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')

    if search_query:
        ads = ads.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    if category_id:
        ads = ads.filter(category_id=category_id)

    context = {
        'ads': ads,
        'categories': categories,
        'current_search': search_query,
        'current_category': category_id,
    }
    return render(request, 'ads/home.html', context)

@login_required
def create_ad(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        phone = request.POST['phone']
        category_id = request.POST['category']
        
        # ساخت آگهی
        ad = Ad.objects.create(
            title=title,
            description=description,
            price=price,
            phone=phone,
            category=Category.objects.get(id=category_id),
            user=request.user
        )
        
        # آپلود عکس‌ها (چندتا عکس)
        images = request.FILES.getlist('images')
        for image in images:
            AdImage.objects.create(ad=ad, image=image)
        
        messages.success(request, 'آگهی شما با موفقیت ثبت شد!')
        return redirect('ads:home')
    
    context = {
        'categories': categories,
    }
    return render(request, 'ads/create_ad.html', context)


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    images = ad.images.all()  # همه عکس‌ها
    context = {
        'ad': ad,
        'images': images,
    }
    return render(request, 'ads/ad_detail.html', context)