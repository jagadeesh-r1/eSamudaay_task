from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="IndexPage"),
    path('calculate_order_value',views.calculate,name="OrderCost API")
]