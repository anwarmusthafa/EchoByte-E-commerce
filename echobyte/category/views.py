from django.shortcuts import render, redirect
from .models import Category, Brand
from app_admin.decorators import custom_user_passes_test

@custom_user_passes_test(lambda u: u.is_staff)
def categories(request):
    categories = Category.objects.all()
    context = {'categories' : categories,}
    return render(request, 'categories.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
def brands(request):
    brands = Brand.objects.all()
    context = {'brands': brands}
    return render(request,'brands.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
def add_category(request):
    if request.POST:
        category = request.POST.get('category')
        adding_category = Category.objects.create(name = category)
        return redirect('categories')
    return render(request, 'add_category.html')

@custom_user_passes_test(lambda u: u.is_staff)
def edit_category(request,pk):
    category_instance = Category.objects.get(pk=pk)
    if request.POST:
        category = request.POST.get('category')
        category_instance.name = category
        category_instance.save()
        return redirect('categories')
    return render(request, 'edit_category.html', {'category_instance': category_instance})

@custom_user_passes_test(lambda u: u.is_staff)
def add_brand(request):
    if request.POST:
        brand_name = request.POST.get('brand_name')
        adding_brand = Brand.objects.create(brand = brand_name)
        return redirect('brands') 
    return render(request, 'add_brand.html')

@custom_user_passes_test(lambda u: u.is_staff)
def edit_brand(request,pk):
    brand_instance = Brand.objects.get(pk=pk)
    if request.POST:
        brand_name = request.POST.get('brand_name')
        brand_instance.brand = brand_name
        brand_instance.save()
        return redirect('brands')
    return render(request, 'edit_brand.html', {'brand_instance':brand_instance})

@custom_user_passes_test(lambda u: u.is_staff)
def block_category(request,pk):
    if request.POST:
        if request.POST:
            status = request.POST.get('status')
            category_instance = Category.objects.get(pk=pk)
            category_instance.is_listed = status
            category_instance.save()
            return redirect('categories')
        
@custom_user_passes_test(lambda u: u.is_staff)
def block_brand(request,pk):
        if request.POST:
            status = request.POST.get('status')
            brand_instance = Brand.objects.get(pk=pk)
            brand_instance.is_listed = status
            brand_instance.save()
            return redirect('brands')






