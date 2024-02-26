from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from customer.models import *
from order.models import *
from django.db.models import Q, Sum
from datetime import datetime
from django.utils import timezone
import xlwt
from django.utils.timezone import make_naive
@never_cache
# @user_passes_test(lambda u: u.is_authenticated and u.is_staff)
def admin_login(request):
    error_message = None
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
    
            if user and user.is_staff:
                login(request, user)
                return redirect('admin_home')
            else:
                raise ValueError("Invalid Credentials")
    except Exception as e:
        # Handle specific exception types if needed
        error_message = str(e)
    context = {'error_message': error_message}
    return render(request, 'admin_login.html', context)

@never_cache
@login_required(login_url='admin_login')
def admin_home(request):
    total_order_count = OrderItem.objects.filter().count()
    total_amount = OrderItem.objects.filter(
    Q(payment_method='cod', order_status=3) | Q(payment_method ='online', order_status__lt=5)
    ).aggregate(
    total_amount=Sum('amount')
    )
    total_discount = Order.objects.aggregate(total_discount=Sum('discount_amount'))
    pending_shipping_count = OrderItem.objects.filter(order_status = 1).count()
    pending_delivery_count =  OrderItem.objects.filter(order_status = 2).count()
    pending_return_request = OrderItem.objects.filter(order_status = 4).count()

    cod_count = OrderItem.objects.filter(payment_method = 'cod').count()
    online_count = OrderItem.objects.filter(payment_method = 'online').count()
    cod_percentage = (cod_count / (cod_count + online_count) * 100 )
    online_percentage = (online_count / (cod_count + online_count) * 100 )
    payment_percentage = [cod_percentage,online_percentage]

    recent_orders = OrderItem.objects.order_by('-created_at')[:10]
   


    context = {'total_order_count':total_order_count,
               'total_amount': total_amount['total_amount'],
               'total_discount':total_discount['total_discount'],
               'pending_shipping_count':pending_shipping_count,
               'pending_delivery_count': pending_delivery_count,
               'pending_return_request':pending_return_request,
               'payment_percentage':payment_percentage,
               'recent_orders':recent_orders}
    return render(request, 'admin_home.html',context)

@never_cache
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def customers_list(request):
     customers = User.objects.exclude(pk = 1)
     context = {'customers': customers}
     return render(request, 'customers_list.html', context)
@login_required(login_url='admin_login')
def delete_status(request, pk):
    if request.POST:
        delete_status = int(request.POST.get('delete_status'))
        print(delete_status)
        user = get_object_or_404(Customer,user_id=pk)
        if delete_status == 0:
            user.delete_status = 0
        else:
            user.delete_status = 1
        user.save()
    return redirect('customers_list')
def sales_report(request):
    sales = None
    if request.method == 'POST':
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        # Convert string dates to datetime objects
        start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
        sales = OrderItem.objects.filter(order_status=3,created_at__range=[start_date, end_date])
    context = {'sales':sales}
    return render(request,'sales_report.html', context)

def download_excel(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
    end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xls"'

    # Create a new workbook and add a worksheet
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report')

    # Write header row
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Order id', 'Customer', 'Product', 'Qty', 'Amount', 'Date']
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, font_style)

    # Write data rows
    rows = OrderItem.objects.filter(order_status=3,created_at__range=[start_date, end_date])
    for row_num, row in enumerate(rows, start=1):
        ws.write(row_num, 0, row.id)
        ws.write(row_num, 1, row.order.owner.customer.name )
        ws.write(row_num, 2, f"{row.product.product.brand} {row.product.product.title} {row.product.variant_name}")
        ws.write(row_num, 3, row.quantity)
        ws.write(row_num, 4, row.amount)
        created_at_naive = make_naive(row.created_at)
        formatted_date = created_at_naive.strftime('%d/%m/%Y')
        ws.write(row_num, 5, formatted_date)

    # Save the workbook content to the HttpResponse object
    wb.save(response)
    
    return response








    
