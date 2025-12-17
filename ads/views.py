from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ad, Category, AdImage

def home(request):
    ads = Ad.objects.all().order_by('-created_at')
    context = {
        'ads': ads,
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

def ad_details(request,pk):
    ad = get_object_or_404(Ad, pk=pk)
    images = ad.images.all() #عکس ها
    context = {
        'ad': ad,
        'images': images,
        
    }
    return render(request, 'ads/ad_detail',context)