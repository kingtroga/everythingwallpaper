from django.shortcuts import render, get_object_or_404
from product.models import ProductItem, Category
from django.core.cache import cache
from cart.cart import Cart
from django.core.paginator import Paginator

def index(request):
    # cache categories
    categories = cache.get('categories')
    if not categories:
        categories = list(Category.objects.values('id', 'name', 'slug'))
        cache.set('categories', categories, timeout=3600)

    products  = ProductItem.objects.all()
    cart = Cart(request)


    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)


    query = request.GET.get('query', '')

    if query:
        products = products.filter(name__icontains=query)


    # Paginate products
    paginator = Paginator(products.order_by('name') , 6)  # Show 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)


    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category,
        'items_in_cart': len(cart)
    }

    return render(request, 'core/index.html', context)

def product_item(request, pk):
    categories = cache.get('categories')
    if not categories:
        categories = list(Category.objects.values('id', 'name', 'slug'))
        cache.set('categories', categories, timeout=3600)
    product = get_object_or_404(ProductItem, pk=pk)
    cart = Cart(request)

    add_to_cart = request.GET.get('add_to_cart', 'False')

    if add_to_cart == 'True' :
        cart.add(product.product_code)
   
    context = {
        'product':product,
        'categories': categories,
        'items_in_cart': len(cart)
    }
    return render(request, 'core/product_item.html', context)

def custom_404_view(request, exception):
    categories = cache.get('categories')
    if not categories:
        categories = list(Category.objects.values('id', 'name', 'slug'))
        cache.set('categories', categories, timeout=3600)
    cart = Cart(request)

    context = {
        'categories': categories,
        'items_in_cart': len(cart)
    }
    return render(request, 'core/404.html', context, status=404)

def custom_500_view(request):
    categories = cache.get('categories')
    if not categories:
        categories = list(Category.objects.values('id', 'name', 'slug'))
        cache.set('categories', categories, timeout=3600)
    cart = Cart(request)

    context = {
        'categories': categories,
        'items_in_cart': len(cart)
    }
    return render(request, 'core/500.html', context, status=500)

