from .models import CartItems, OrderItem, Wishlist

def cart_items_count(request):
    if request.user.is_authenticated:
        cart_items_count = CartItems.objects.filter(cart__owner=request.user).count()
    else:
        cart_items_count = 0
    return {'cart_items_count': cart_items_count}
def total_order_count(request):
    if request.user.is_authenticated:
        total_order_count = OrderItem.objects.filter(order__owner = request.user).count()
    else:
        total_order_count = 0
    return {'total_order_count': total_order_count}
def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user = request.user).count()
    else:
        wishlist_count = 0
    return {'wishlist_count': wishlist_count}
def cancelled_order_count(request):
    if request.user.is_authenticated:
        cancelled_order_count = OrderItem.objects.filter(order__owner = request.user, order_status = -1).count()
    else:
        cancelled_order_count = 0
    return{'cancelled_order_count':cancelled_order_count}

