from django.shortcuts import render
from .models import Banner
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def banners(request):
    banners = Banner.objects.all()
    context = {'banners':banners}
    return render(request,'banners.html',context)
def add_banner(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            heading = request.POST.get('heading')
            order = request.POST.get('order')
            start_price = request.POST.get('startPrice')
            start_date = request.POST.get('startDate')
            end_date = request.POST.get('endDate')
            # Assuming you're using Django forms for image upload, handle it accordingly
            image = request.FILES.get('image')
            
            # Assuming Banner is your model
            banner = Banner.objects.create(
                banner_name=name,
                banner_heading=heading,
                banner_order=order,
                starting_price=start_price,
                start_date=start_date,
                expiry_date=end_date,
                banner_image=image
            )
            # You might want to redirect the user to a success page or another view
            return redirect('banners')
        except Exception as e:
            # Add an error message using Django's messaging framework
            messages.error(request, f"An error occurred while adding the banner: {e}")
            return render(request, 'add_banner.html')
    return render(request, 'add_banner.html')
def change_banner_status(request,pk):
    if request.POST:
        status = request.POST.get('status')
        banner = Banner.objects.get(pk=pk)
        banner.is_listed = status
        banner.save()
    return redirect('banners')
def delete_banner(request,pk):
    banner = Banner.objects.get(pk=pk)
    banner.delete()
    return redirect('banners')
