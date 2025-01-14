from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from product.models import ProductItem
from .models import Order, OrderItem
import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from pypaystack import Transaction


def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []

    for item in cart.cart.values():
        product = item
        total_price += (int(product['product_price']) * int(product['quantity']))

        obj = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product['product_name']
                },
                'unit_amount': int(product['product_price'])
            },
            'quantity': item['quantity'],
        }

        items.append(obj)

   
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.0.1:8000/cart/success/',
        cancel_url='http://127.0.0.1:8000/cart/'
    )

    payment_intent = session.payment_intent

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    phone = data['phone']

    order = Order.objects.create(
            first_name = first_name,
            last_name = last_name,
            email=email,
            address=address,
            zipcode=zipcode,
            place=place,
            phone=phone
        )
    
    order.payment_intent = payment_intent
    order.paid_amount = total_price
    order.paid = True
    order.save()



    
    for item in cart.cart.values():
        product = get_object_or_404(ProductItem, product_code=str(item['id']))
        quantity = int(item['quantity'])
        price = quantity * item['product_price']

        item = OrderItem.objects.create(
            order=order,
            product=product,
            price=price,
            quantity=quantity)
        
    cart.clear()
        
    return JsonResponse({
        'session': session, 'order': payment_intent
    })

def verify_and_save_order(request, transaction_id):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = sum(
        int(item['product_price']) * int(item['quantity'])
        for item in cart.cart.values()
    )

    # Verify the transaction with Paystack
    transaction = Transaction(authorization_key=settings.PAYSTACK_API_KEY_HIDDEN)
    response = transaction.verify(reference=transaction_id)

    if response[0] and response[3]['status'] == 'success':
        # Create the order
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        address = data['address']
        zipcode = data['zipcode']
        place = data['place']
        phone = data['phone']

        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            zipcode=zipcode,
            place=place,
            phone=phone,
            paid_amount=total_price,
            paid=True
        )

        # Create order items
        for item in cart.cart.values():
            product = get_object_or_404(ProductItem, product_code=str(item['id']))
            quantity = int(item['quantity'])
            price = quantity * int(item['product_price'])

            OrderItem.objects.create(
                order=order,
                product=product,
                price=price,
                quantity=quantity
            )

        # Clear the cart
        cart.clear()

        # Respond with success
        return JsonResponse({'status': 'success', 'message': 'Order placed successfully.'})
    else:
        # Respond with error
        return JsonResponse({'status': 'error', 'message': 'Transaction verification failed.'})
