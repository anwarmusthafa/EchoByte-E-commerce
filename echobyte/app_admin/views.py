from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from customer.models import Customer
from category.models import Brand,ProcessorBrand
from product.models import Product,ProductVariant, ProductImage
@never_cache
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
    return render(request, 'admin_home.html')

@never_cache
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def customers_list(request):
     customers = User.objects.exclude(pk = 1)
     context = {'customers': customers}
     return render(request, 'customers_list.html', context)
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
def list_product(request):
    products = Product.objects.all().order_by('pk')
    for product in products:
        print(product.images.all())
    context = {'products':products}
    return render(request,'list_product.html', context)
def product_delete(request,pk):
    if request.POST:
        delete_status = int(request.POST.get('delete_status'))
        print(delete_status)
        product = get_object_or_404(Product,pk=pk)
        if delete_status == 0:
            product.delete_status = 0
        else:
            product.delete_status = 1
        product.save()
    return redirect('list_product')
def add_product(request):
    existing_brands = Brand.objects.filter(is_listed=True)
    existing_processor_brands = ProcessorBrand.objects.filter(is_listed=True)
    category_choices = Product.CATEGORY_CHOICES

    error_message = None
    success_message = None

    if request.method == 'POST':
        try:
            brand_id = request.POST.get('brand')
            category = request.POST.get('category')  # Corrected typo in 'category'
            title = request.POST.get('title')
            processor_brand_id = request.POST.get('processor-brand')
            processor = request.POST.get('processor')
            display = request.POST.get('display')
            front_camera = request.POST.get('front-camera')
            back_camera = request.POST.get('back-camera')
            priority = request.POST.get('priority')
            battery_capacity = request.POST.get('battery')
            description = request.POST.get('description')  # Corrected typo in 'description'

            # Get Brand and ProcessorBrand instances
            brand_to_add = Brand.objects.get(pk=brand_id) if brand_id else None
            processor_brand_to_add = ProcessorBrand.objects.get(pk=processor_brand_id) if processor_brand_id else None

            # Create a new Product entry
            adding_product = Product.objects.create(
                brand=brand_to_add,
                category=category,
                title=title,
                processor_brand=processor_brand_to_add,
                processor=processor,
                display=display,
                front_camera=front_camera,
                back_camera=back_camera,
                priority=priority,
                battery_capacity=battery_capacity,
                description=description
            )

            for i in range(1, 6):
                image_file = request.FILES.get(f"image-{i}")
                if image_file:
                    # Save the image to the ProductImage model
                    product_image = ProductImage.objects.create(
                        product=adding_product,
                        image=image_file,
                        image_order=i
                    )
                else:
                    print("image file not available")

            success_message = "Product added successfully!"

        except Brand.DoesNotExist:
            error_message = "Selected brand does not exist."
        except ProcessorBrand.DoesNotExist:
            error_message = "Selected processor brand does not exist."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    context = {
        'category_choices': category_choices,
        'existing_brands': existing_brands,
        'existing_processor_brands': existing_processor_brands,
        'error_message': error_message,
        'success_message': success_message,
    }

    return render(request, 'add_product.html', context)

def add_variant(request):
    existing_products = Product.objects.filter(delete_status=1)
    ram_choices = ProductVariant.RAM_CHOICES
    storage_choices = ProductVariant.STORAGE_CHOICES
    error_message = None
    success_message = None

    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')  
            variant_name = request.POST.get('variant-name')
            ram = request.POST.get('ram')
            internal_storage = request.POST.get('internal-storage')
            colour = request.POST.get('colour')
            original_price = request.POST.get('original-price')  
            selling_price = request.POST.get('selling-price')
            stock = request.POST.get('stock')

            product = Product.objects.get(pk=product_id)  # Retrieve the selected product

            # Create a new ProductVariant entry
            adding_variant = ProductVariant.objects.create(
                product=product,
                variant_name=variant_name,
                ram=ram,
                storage=internal_storage,
                colour=colour,
                original_price=original_price,
                selling_price=selling_price,
                stock=stock
            )

            success_message = "Variant added successfully!"

        except Product.DoesNotExist:
            error_message = "Selected product does not exist."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    context = {
        'existing_products': existing_products,
        'ram_choices': ram_choices,
        'storage_choices': storage_choices,
        'error_message': error_message,
        'success_message': success_message,
    }

    return render(request, 'add_variant.html', context)
def list_variants(request):
    variants = ProductVariant.objects.all
    context = {'variants': variants}
    return render(request, 'list_variants.html', context)
def  variant_block(request,pk):
    if request.POST:
        block_status = int(request.POST.get('block_status'))
        print(block_status)
        variant = get_object_or_404(ProductVariant,pk=pk)
        if block_status == 0:
            variant.is_listed = True
        else:
            variant.is_listed = False
        variant.save()
    return redirect('list_variants')

def edit_product(request, pk):
    # Use get_object_or_404 to handle the case where the product does not exist
    product = get_object_or_404(Product, pk=pk)
    images = ProductImage.objects.filter(product=product)
    existing_brands = Brand.objects.filter(is_listed=True)
    existing_processor_brands = ProcessorBrand.objects.filter(is_listed=True)
    category_choices = Product.CATEGORY_CHOICES
    error_message = None
    success_message = None

    if request.method == 'POST':
        try:
            brand_id = request.POST.get('brand')
            category = request.POST.get('category')
            title = request.POST.get('title')
            processor_brand_id = request.POST.get('processor-brand')
            processor = request.POST.get('processor')
            display = request.POST.get('display')
            front_camera = request.POST.get('front-camera')
            back_camera = request.POST.get('back-camera')
            priority = request.POST.get('priority')
            battery = request.POST.get('battery')
            description = request.POST.get('description')

            # Get Brand and ProcessorBrand instances
            brand_to_add = Brand.objects.get(pk=brand_id) if brand_id else None
            processor_brand_to_add = ProcessorBrand.objects.get(pk=processor_brand_id) if processor_brand_id else None

            # Update or create a new Product entry
            editing_product, created = Product.objects.update_or_create(
                pk=pk,
                defaults={
                    'brand': brand_to_add,
                    'category': category,
                    'title': title,
                    'processor_brand': processor_brand_to_add,
                    'processor': processor,
                    'display': display,
                    'front_camera': front_camera,
                    'back_camera': back_camera,
                    'priority': priority,
                    'battery_capacity': battery,
                    'description': description
                }
            )

            # Iterate over the range of image orders (1 to 5)
            for i in range(1, 6):
                # Get the new image file from the request
                image_file = request.FILES.get(f"image-{i}")
                print(image_file, i)

                if not image_file:
                    print("Image not provided for order", i)
                    continue

                # Check if an existing image exists for the order
                existing_image = editing_product.images.filter(image_order=i).first()

                # If an existing image is found, delete it
                if existing_image:
                    existing_image.image.delete()
                    existing_image.delete()
                    print(f"Deleted existing image for order {i}")

                # Create a new ProductImage
                ProductImage.objects.create(
                    product=editing_product,
                    image_order=i,
                    image=image_file
                )
                print(f"Created new image for order {i}")

            success_message = "Product updated successfully!"

        except Brand.DoesNotExist:
            error_message = "Selected brand does not exist."
        except ProcessorBrand.DoesNotExist:
            error_message = "Selected processor brand does not exist."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    context = {
        'product': product,
        'existing_brands': existing_brands,
        'existing_processor_brands': existing_processor_brands,
        'category_choices': category_choices,
        'images': images,
        'error_message': error_message,
        'success_message': success_message
    }

    return render(request, 'edit_product.html', context)
def edit_variant(request,pk):
    variant = ProductVariant.objects.get(pk=pk)
    existing_products = Product.objects.filter(delete_status=1)
    ram_choices = ProductVariant.RAM_CHOICES
    storage_choices = ProductVariant.STORAGE_CHOICES
    error_message = None
    success_message = None

    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')  
            variant_name = request.POST.get('variant-name')
            ram = request.POST.get('ram')
            internal_storage = request.POST.get('internal-storage')
            colour = request.POST.get('colour')
            original_price = request.POST.get('original-price')  
            selling_price = request.POST.get('selling-price')
            stock = request.POST.get('stock')

            product = Product.objects.get(pk=product_id)  # Retrieve the selected product

            # Create a new ProductVariant entry
            variant.product = product
            variant.variant_name = variant_name
            variant.ram = ram
            variant.storage = internal_storage
            variant.colour = colour
            variant.original_price = original_price
            variant.selling_price = selling_price
            variant.stock = stock

            variant.save() 

            success_message = "Variant updated successfully!"

        except Product.DoesNotExist:
            error_message = "Selected product does not exist."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"


    context = {
        'variant':variant,
        'existing_products': existing_products,
        'ram_choices': ram_choices,
        'storage_choices': storage_choices,
        'error_message': error_message,
        'success_message': success_message,
    }
    return render(request, 'edit_variant.html',context)

    
