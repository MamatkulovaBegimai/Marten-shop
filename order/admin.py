from django.contrib import admin
from order.models import Order, OrderItem, BillingInformation

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')


@admin.register(BillingInformation)
class BillingInformationAdmin(admin.ModelAdmin):
    list_display = ('user', )