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
import io
from reportlab.pdfgen import canvas
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
        user = get_object_or_404(Customer,user_id=pk)
        if delete_status == 0:
            user.delete_status = 0
        else:
            user.delete_status = 1
        user.save()
    return redirect('customers_list')
def sales_report(request):
    sales = None
    message = None
    if 'start_date' in request.session:
        del request.session['start_date']
    if 'end_date' in request.session:
        del request.session['end_date']
    if 'month' in request.session:
        del request.session['month']
    if request.method == 'POST':
        start_date_str = request.POST.get('start-date')
        end_date_str = request.POST.get('end-date')
        month = int(request.POST.get('month'))
        year = datetime.now().year
        if month > 0:
            start_date_str = f"{year}-{month:02d}-01"
            if month == 12:
                end_date_str = f"{year + 1}-01-01"
            else:
                end_date_str = f"{year}-{month + 1:02d}-01"

        if start_date_str and end_date_str:  # Check if both start and end dates are provided
            request.session['start_date'] = start_date_str
            request.session['end_date'] = end_date_str
            request.session['month'] = month

            # Parse start and end dates from strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Convert start and end dates to timezone-aware datetime objects
            start_date = timezone.make_aware(start_date)
            end_date = timezone.make_aware(end_date)

            # Filter sales based on the provided date range
            sales = OrderItem.objects.filter(order_status=3, created_at__range=[start_date, end_date])
            if not sales:
                message = "No sales in these dates"
        else:
            message = "Please provide both start and end dates."

    context = {'sales': sales, 'message': message}
    return render(request, 'sales_report.html', context)

def download_excel(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    month = request.session.get('month',0)
    year = datetime.now().year
    if month > 0:
        start_date = timezone.make_aware(datetime(year, month, 1))
        if month == 12:
            end_date = timezone.make_aware(datetime(year + 1, 1, 1))
        else:
            end_date = timezone.make_aware(datetime(year, month + 1, 1))

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xls"'

    # Create a new workbook and add a worksheet
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report')

    # Write header row
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Order id', 'Customer', 'Product', 'Qty', 'Total Amount', 'Discount Amount', 'Net Amount', 'Date']
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, font_style)

    # Write data rows
    rows = OrderItem.objects.filter(order_status=3, created_at__range=[start_date, end_date])
    for row_num, row in enumerate(rows, start=1):
        ws.write(row_num, 0, row.id)
        ws.write(row_num, 1, row.order.owner.customer.name)
        ws.write(row_num, 2, f"{row.product.product.brand} {row.product.product.title} {row.product.variant_name}")
        ws.write(row_num, 3, row.quantity)
        ws.write(row_num, 4, row.total_amount)
        ws.write(row_num, 5, row.discount_amount)
        ws.write(row_num, 6, row.amount)
        created_at_naive = make_naive(row.created_at)
        formatted_date = created_at_naive.strftime('%d/%m/%Y')
        ws.write(row_num, 7, formatted_date)

    # Save the workbook content to the HttpResponse object
    wb.save(response)

    return response
from decimal import Decimal

def download_pdf(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
    end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))

    # Create a PDF buffer
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Set up PDF
    p.setFont("Helvetica-Bold", 16)  # Set title font to bold and increase font size
    p.drawString(200, 750, "EchoByte Sales Report")  # Position the title
    p.setFont("Helvetica", 12)  # Set regular font size for content

    # Write PDF content
    orders = OrderItem.objects.filter(order_status=3, created_at__range=[start_date, end_date])

    # Define column widths
    col_widths = [70, 70, 250, 30, 70, 60]  # Adjust as needed

    # Initialize starting y-coordinate
    y = 700

    # Write header row
    header = ['Order id', 'Customer', 'Product', 'Qty', 'Amount', 'Date']
    x = 20
    for i, col in enumerate(header):
        p.drawString(x, y, col)
        x += col_widths[i]  # Move x-coordinate to the start of next column
    y -= 20  # Move y-coordinate to start the content below the header

    # Write data rows
    total_amount = Decimal(0)
    for order in orders:
        x = 20
        p.drawString(x, y, str(order.id))
        x += col_widths[0]
        p.drawString(x, y, str(order.order.owner.customer.name))
        x += col_widths[1]
        product_info = f"{order.product.product.brand} {order.product.product.title} ({order.product.variant_name})"
        p.drawString(x, y, product_info)
        x += col_widths[2]
        p.drawString(x, y, str(order.quantity))
        x += col_widths[3]
        p.drawString(x, y, str(order.amount))
        total_amount += order.amount  # Add order amount to total
        x += col_widths[4]
        created_at_naive = make_naive(order.created_at)
        formatted_date = created_at_naive.strftime('%d/%m/%Y')
        p.drawString(x, y, formatted_date)
        y -= 20  # Move y-coordinate to the next row

    # Write total amount
    p.drawString(400, y - 40, f"Total Amount: {total_amount}")

    # Close PDF
    p.showPage()
    p.save()

    # Get PDF content from the buffer and return as response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    return response











    
