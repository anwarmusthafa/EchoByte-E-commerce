from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from category.models import Brand,Category
from product.models import Product,ProductVariant, ProductImage
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from order.models import CartItems,Wishlist
from app_admin.decorators import custom_user_passes_test

def all_products(request):
    try:
        query = request.GET.get('search')
        category = request.GET.get('category')
        sort_by = request.GET.get('sort')
        min_price = request.GET.get('min-price')
        max_price = request.GET.get('max-price')
        # Base queryset
        variants = ProductVariant.objects.exclude(
        Q(product__delete_status=0) |
        Q(product__is_listed=False) |
        Q(product__category__is_listed=False) |
        Q(is_listed=False)
        ).order_by('-product__priority')

        if request.user.is_authenticated:
            wishlist_product_pks = list(Wishlist.objects.filter(user=request.user).values_list('product__pk', flat=True))
        else:
            wishlist_product_pks = None
        
        if sort_by == 'latest':
            variants = variants.order_by('-product__created_at')
        if sort_by == 'lowest-price':
            variants = variants.order_by('selling_price')
        if sort_by == 'highest-price':
            variants = variants.order_by('-selling_price')
        if sort_by == 'relevance':
            variants = variants.order_by('-product__priority')

        # Apply search filter
        if query:
            variants = variants.filter(Q(product__title__icontains=query) | Q(product__brand__brand__icontains=query))
        
        if category:
            categories = category.split(',')
            variants = variants.filter(product__category__name__in=categories)
        if min_price:
                variants = variants.filter(selling_price__gte=min_price)
        if max_price:
                variants = variants.filter(selling_price__lte=max_price)
        product_count = variants.count()

        # Paginate the queryset
        paginator = Paginator(variants, 4)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context = {
    'variants': page_obj,
    'query': query,
    'sort_by': sort_by,
    'categories': category.split(',') if category else [],  # Convert category string to list
    'min_price': min_price,
    'max_price': max_price,
    'wishlist_product_pks': wishlist_product_pks,
    'product_count': product_count,
}

    except ObjectDoesNotExist as e:
        context = {
            'error_message': f"Object does not exist: {str(e)}"
        }
    except Exception as e:
        context = {
            'error_message': f"An error occurred: {str(e)}"
        }
    return render(request, 'all_products.html', context)

def product_detail(request, pk):
    cart_item = None
    wishlist = None 
    
    try:
        product = get_object_or_404(ProductVariant, id=pk)
        if request.user.is_authenticated:
            
            try:
                wishlist = Wishlist.objects.get(user=request.user, product=product)
            except Wishlist.DoesNotExist:
                pass
        if request.user.is_authenticated:
            cart_item = CartItems.objects.filter(cart__owner=request.user, product=product)
        variants = product.product.variants.filter(is_listed=True).order_by('selling_price')
        product_images = ProductImage.objects.filter(product=product.product)
        context = {
            'product': product,
            'product_images': product_images,
            'variants': variants,
            'cart_item': cart_item,
            'wishlist': wishlist,
        }
    except ObjectDoesNotExist as e:
        context = {
            'error_message': f"Object does not exist: {str(e)}"
        }

    except Exception as e:
        context = {
            'error_message': f"An error occurred: {str(e)}"
        }
    return render(request, 'product-detail.html', context)


@custom_user_passes_test(lambda u: u.is_staff)
def list_product(request):
    products = Product.objects.all().order_by('pk')
    page = 1
    if request.GET:
        page = request.GET.get('page',1)
    product_paginator = Paginator(products,10)
    products = product_paginator.get_page(page)
    context = {'products':products}
    return render(request,'list_product.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
def product_delete(request,pk):
    if request.POST:
        delete_status = int(request.POST.get('delete_status'))
        
        product = get_object_or_404(Product,pk=pk)
        if delete_status == 0:
            product.delete_status = 0
        else:
            product.delete_status = 1
        product.save()
    return redirect('list_product')

@custom_user_passes_test(lambda u: u.is_staff)
def add_product(request):
    existing_brands = Brand.objects.filter(is_listed=True)
    existing_categories = Category.objects.filter(is_listed=True)
    error_message = None
    success_message = None

    if request.method == 'POST':
        try:
            brand_id = request.POST.get('brand')
            category_id = request.POST.get('category') 
            title = request.POST.get('title')
            processor = request.POST.get('processor')
            display = request.POST.get('display')
            front_camera = request.POST.get('front-camera')
            back_camera = request.POST.get('back-camera')
            priority = request.POST.get('priority')
            battery_capacity = request.POST.get('battery')
            description = request.POST.get('description')

            brand_to_add = Brand.objects.get(pk=brand_id) if brand_id else None
            category_to_add = Category.objects.get(pk=category_id) if category_id else None

            adding_product = Product.objects.create(
                brand=brand_to_add,
                category=category_to_add,
                title=title,
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
                    product_image = ProductImage.objects.create(
                        product=adding_product,
                        image=image_file,
                        image_order=i
                    )
            success_message = "Product added successfully!"
        except Brand.DoesNotExist:
            error_message = "Selected brand does not exist."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    context = {
        'existing_brands': existing_brands,
        'existing_categories':existing_categories,
        'error_message': error_message,
        'success_message': success_message,
    }

    return render(request, 'add_product.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
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

            product = Product.objects.get(pk=product_id) 

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

@custom_user_passes_test(lambda u: u.is_staff)
def list_variants(request):
    variants = ProductVariant.objects.all
    context = {'variants': variants}
    return render(request, 'list_variants.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
def  variant_block(request,pk):
    if request.POST:
        block_status = int(request.POST.get('block_status'))
        variant = get_object_or_404(ProductVariant,pk=pk)
        if block_status == 0:
            variant.is_listed = True
        else:
            variant.is_listed = False
        variant.save()
    return redirect('list_variants')

@custom_user_passes_test(lambda u: u.is_staff)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = ProductImage.objects.filter(product=product)
    categories = Category.objects.filter(is_listed=True)
    existing_brands = Brand.objects.filter(is_listed=True)
    error_message = None
    success_message = None
    if request.method == 'POST':
        try:
            brand_id = request.POST.get('brand')
            category = request.POST.get('category')
            title = request.POST.get('title')
            processor = request.POST.get('processor')
            display = request.POST.get('display')
            front_camera = request.POST.get('front-camera')
            back_camera = request.POST.get('back-camera')
            priority = request.POST.get('priority')
            battery = request.POST.get('battery')
            description = request.POST.get('description')

            brand_to_add = Brand.objects.get(pk=brand_id) if brand_id else None
            category_to_add = Category.objects.get(name = category) if category else None

            editing_product, created = Product.objects.update_or_create(
                pk=pk,
                defaults={
                    'brand': brand_to_add,
                    'category': category_to_add,
                    'title': title,
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
                if not image_file:
                    continue
                # Check if an existing image exists for the order
                existing_image = editing_product.images.filter(image_order=i).first()

                # If an existing image is found, delete it
                if existing_image:
                    existing_image.image.delete()
                    existing_image.delete()
                ProductImage.objects.create(
                    product=editing_product,
                    image_order=i,
                    image=image_file
                )

            success_message = "Product updated successfully!"

        except Brand.DoesNotExist:
            error_message = "Selected brand does not exist."
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
    context = {
        'product': product,
        'existing_brands': existing_brands,
        'images': images,
        'error_message': error_message,
        'success_message': success_message,
        'categories' : categories
    }
    return render(request, 'edit_product.html', context)

@custom_user_passes_test(lambda u: u.is_staff)
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

            product = Product.objects.get(pk=product_id)

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
