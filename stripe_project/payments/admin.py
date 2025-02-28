from django.contrib import admin
from .models import Item, Discount, Tax, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')
    search_fields = ('name',)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price', 'discount', 'tax')
    search_fields = ('id',)
    list_filter = ('discount', 'tax')