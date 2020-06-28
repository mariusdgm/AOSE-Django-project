from django.contrib import admin
from .models import FoodDish, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Date", {"fields": ["order_date"]}),
        ("Items", {"fields": ["items"]}),
        ("Details", {"fields":["ordered", "total_price"]}),
    ]

# Register your models here.
admin.site.register(FoodDish)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)