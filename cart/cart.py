from django.conf import settings
from product.models import ProductItem
from django.shortcuts import get_object_or_404

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        # the keys in the cart is the product_id of 
        # each product
        for p in self.cart.keys:
            self.cart[str(p)]['product'] = ProductItem.objects.get(product_code=p)

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']

        yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, 
            product_id, 
            quantity=1, 
            update_quantity=False):
        product_id = str(product_id)

        if product_id not in self.cart and product_id != '1':
            self.cart[product_id] = {
                'quantity': 1, 
                'id': product_id,
                'product_name': ProductItem.objects.get(product_code=product_id).name,
                'product_image':ProductItem.objects.get(product_code=product_id).images.first().image.url,
                'product_price': float(ProductItem.objects.get(product_code=product_id).price),
                }
            self.cart[product_id]['total_price'] = float(self.cart[product_id]['quantity'] * ProductItem.objects.get(product_code=product_id).price)
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            self.cart[product_id]['total_price'] = float(self.cart[product_id]['quantity'] * ProductItem.objects.get(product_code=product_id).price)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)

        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            self.cart.pop(product_id)
            self.save()
    
    def empty(self):
        cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True