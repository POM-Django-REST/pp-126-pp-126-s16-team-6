from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),  # For librarian to view all orders
    path('my-orders/', views.UserOrderListView.as_view(), name='user_orders'),  # For users to view their orders
    path('order/create-order/', views.create_order, name='create_order'),
    path('close-order/<int:order_id>/', views.close_order, name='close_order'),  # For librarian to close an order
]
