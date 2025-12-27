from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ad, Category, AdImage
import django.db.models as models
from django.core.paginator import Paginator


def home(request):
    ads = Ad.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    # گرفتن پارامترهای جستجو و فیلتر از GET
    
    search_query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')

    if search_query:
        ads_list = ads.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    if category_id:
        ads = ads.filter(category_id=category_id)

    # صفحه‌بندی: ۱۲ آگهی در هر صفحه
    paginator = Paginator(ads, 12)
    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)
    
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

@login_required
def edit_ad(request,pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user :
        messages.error(request, 'شما اجازه ویرایش این آگهی را ندارید.')
        return redirect ('ads:ad_detail', pk=pk)
    

    categories = Category.objects.all

    if request.method == 'POST':
        ad.title = request.POST['title']
        ad.description = request.POST['description']
        ad.price = request.POST['price']
        ad.phone = request.POST['phone']
        ad.category = Category.objects.get(id=request.POST['category'])
        ad.save()

        #اگر بخواد عکس های قبلی حذف کنه
        if request.POST.get('delete_images'):
            ad.images.all().delete()

        #آپلود عکس های جدید
        images = request.FILES.getlist('images')
        for image in images:
            AdImage.objects.create(ad=ad, image=image)

        messages.success(request, 'ویرایش انجام شد.')
        return redirect ('ads:ad_detail', pk=pk)
    
    context = {
        'ad':ad,
        'categories': categories,
    }
    return render(request, 'ads/delete_ad.html', context)

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    
    # فقط صاحب آگهی اجازه حذف داره
    if ad.user != request.user:
        messages.error(request, 'شما اجازه حذف این آگهی را ندارید.')
        return redirect('ads:ad_detail', pk=pk)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'آگهی با موفقیت حذف شد.')
        return redirect('ads:home')
    
    context = {'ad': ad}
    return render(request, 'ads/delete_ad.html', context)


@login_required
def my_ads(request):
    ads_list = Ad.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(ads_list, 12)  # ۱۲ آگهی در هر صفحه
    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)
    
    context = {
        'ads': ads,
    }
    return render(request, 'ads/my_ads.html', context)

