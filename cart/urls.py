from django.urls import path
from .views import cart, checkout, success

urlpatterns = [
    path('', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('success/', success, name='success')
]