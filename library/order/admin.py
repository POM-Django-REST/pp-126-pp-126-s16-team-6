from django.contrib import admin
from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['id', 'book__name', 'user__email', 'user__last_name']
    list_filter = ['book', 'user']
    list_display = ['id', 'book', 'user', 'created_at', 'end_at']


admin.site.register(Order, OrderAdmin)
