from django.urls import path
from .views import start_order, verify_and_save_order


urlpatterns = [
    path('start_order/', start_order, name='start_order'),
    path('verify_and_save_order/<str:transaction_id>/', verify_and_save_order, name='verify_and_save_order' )
]