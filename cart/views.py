from django.shortcuts import render
from .cart import Cart
from product.models import Category
from django.conf import settings
from django.core.cache import cache


def cart(request):
    categories = cache.get('categories')
    if not categories:
        categories = list(Category.objects.values('id', 'name', 'slug'))
        cache.set('categories', categories, timeout=3600)
    cart1 = Cart(request)
    operation = request.GET.get('operation', '')
    item = request.GET.get('item', '')

    if operation and item:
        if operation == 'sub':
            # if the item has already been deleted
            if cart1.cart.get(item):
                cart1.cart[item]['quantity'] = cart1.cart[item]['quantity'] - 1
                if cart1.cart[item]['quantity'] == 0:
                    cart1.remove(item)
                else:
                    cart1.cart[item]['total_price'] = cart1.cart[item]['quantity'] * cart1.cart[item]['product_price']
                    cart1.save()
            else:
                pass
        elif operation == 'add':
            if cart1.cart.get(item):
                cart1.cart[item]['quantity'] = cart1.cart[item]['quantity'] + 1
                cart1.cart[item]['total_price'] = cart1.cart[item]['quantity'] * cart1.cart[item]['product_price']
                cart1.save()
            else:
                pass

    try:
        total_price_of_items = sum(item['total_price'] for item in cart1.cart.values())
    except KeyError:
        total_price_of_items = 0
    context = {
        'categories': categories,
        'items_in_cart': len(cart1),
        'cart': cart1.cart.values(),
        'total_price_of_items': total_price_of_items,
    }
    return render(request, 'cart/cart.html', context)

def checkout(request):
    pub_key_stripe = settings.STRIPE_API_KEY_PUBLISHABLE
    pub_key_paystack = settings.PAYSTACK_API_KEY_PUBLISHABLE
    categories = Category.objects.all()
    cart = Cart(request)
    

    try:
        total_price_of_items = sum(item['total_price'] for item in cart.cart.values())
    except KeyError:
        total_price_of_items = 0

    context = {
        'categories': categories,
        'items_in_cart': len(cart),
        'total_price_of_items': total_price_of_items,
        'pub_key_stripe':pub_key_stripe,
        'pub_key_paystack':pub_key_paystack,

    }
    return render(request, 'cart/checkout.html', context)

def success(request):
    categories = cache.get('categories')
    if not categories:
        categories = list(Category.objects.values('id', 'name', 'slug'))
        cache.set('categories', categories, timeout=3600)
    cart = Cart(request)

    context = {
        'categories': categories,
        'items_in_cart': len(cart),
    }
    return render(request, 'cart/success.html', context )

    