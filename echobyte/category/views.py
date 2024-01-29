from django.shortcuts import render, redirect
from .models import Category, Brand

# Create your views here.
def categories(request):
    categories = Category.objects.all()
    context = {'categories' : categories,}
    return render(request, 'categories.html', context)
def brands(request):
    brands = Brand.objects.all()
    context = {'brands': brands}
    return render(request,'brands.html', context)
def add_category(request):
    if request.POST:
        category = request.POST.get('category')
        adding_category = Category.objects.create(name = category)
        return redirect('categories')
    return render(request, 'add_category.html')
def edit_category(request,pk):
    if request.POST:
        category = request.POST.get('category')
        category_instance = Category.objects.get(pk=pk)
        category_instance.name = category
        category_instance.save()
        return redirect('categories')
    return render(request, 'edit_category.html')
def add_brand(request):
    if request.POST:
        brand_name = request.POST.get('brand_name')
        adding_brand = Brand.objects.create(brand = brand_name)
        return redirect('brands') 
    return render(request, 'add_brand.html')
def edit_brand(request,pk):
    if request.POST:
        brand_name = request.POST.get('brand_name')
        print(brand_name)
        brand_instance = Brand.objects.get(pk=pk)
        brand_instance.brand = brand_name
        brand_instance.save()
        return redirect('brands')
    return render(request, 'edit_brand.html') 



