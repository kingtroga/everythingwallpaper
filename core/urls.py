from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.product_item, name='product_item')
]