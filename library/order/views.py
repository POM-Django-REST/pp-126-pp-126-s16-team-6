# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Order
from book.models import Book
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import OrderForm

class OrderListView(ListView):
    model = Order
    template_name = "order/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.all()
    

class UserOrderListView(ListView):
    model = Order
    template_name = "order/user_order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')  
    else:
        form = OrderForm()
    return render(request, 'order/create_order.html', {'form': form})

@login_required
def close_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.end_at is None:  
        order.update(end_at=timezone.now())  
        return redirect('order_list')  
    return redirect('order_list')


    