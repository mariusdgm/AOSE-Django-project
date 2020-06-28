from django.db import models
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

class FoodDish(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    likes = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    added_on = models.DateTimeField("date added", default=datetime.now())
    photo_name = models.CharField(max_length=200, default="default-pic.jpg") 
    ingredients = models.TextField(max_length=500, default="salt")
    slug = models.SlugField(default="test-dish")
    showcased = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Food Dishes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("foodster:dish", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("foodster:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_quick_add_to_cart_url(self):
        return reverse("foodster:quick-add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("foodster:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_order_add_to_cart_url(self):
        return reverse("foodster:order-add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_order_remove_from_cart_url(self):
        return reverse("foodster:order-remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_order_remove_from_cart_whole_item_url(self):
        return reverse("foodster:order-remove-from-cart-whole-item", kwargs={
            'slug': self.slug
        })
    

class OrderItem(models.Model):
    item = models.ForeignKey(FoodDish, 
                            on_delete=models.CASCADE, 
                            blank=True,
                            null=True)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
        
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)

    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return f"{self.user.username} ordered on {self.order_date}"

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total