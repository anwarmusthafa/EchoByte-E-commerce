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


