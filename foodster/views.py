from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import DetailView, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NewUserForm

from .models import FoodDish, OrderItem, Order


# Create your views here.
def homepage(request):
    showcased_objects = FoodDish.objects.filter(showcased=True)

    return render(request=request, 
                  template_name="foodster/homepage.html",
                  context={"dishes": showcased_objects})

                 

def menu(request):
    return render(request=request, 
                  template_name="foodster/menu.html",
                  context={"dishes": FoodDish.objects.all})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as: {username}")
            return redirect("foodster:menu")
        else:
            for msg in form.error_messages:
                # messages.error(request, f"{msg}: {form.error_messages[msg]}")
                messages.error(request, "An error occured when validating form (password mismatch, invalid email)")

    form = NewUserForm()
    return render(request, 
                  "foodster/register.html",
                   context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out succesfully")
    return redirect("foodster:menu")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username is not None and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as: {username}")
                    return redirect("foodster:menu")
                else:
                    messages.error(request, "Invalid username or password")
                    
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")


    form = AuthenticationForm()
    return render(request,
                  "foodster/login.html",
                  context={"form":form})

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        # try:
        order, created = Order.objects.get_or_create(
                            user=self.request.user, 
                            ordered=False,)
        return render(self.request, 
                        'foodster/order_summary.html',
                        context={"order": order})
        # except:
        #     messages.error(self.request, "There is no active order")
        #     return redirect("/")
        

@login_required
def base_add_to_cart(request, slug):
    item = get_object_or_404(FoodDish, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
            
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=order_date)
        order.items.add(order_item)

    order.save()
    
    messages.info(request, f"{item.name} added to basket")

def add_to_cart(request, slug):
    base_add_to_cart(request, slug)
    return redirect("foodster:dish", slug=slug)

def quick_add_to_cart(request, slug):
    base_add_to_cart(request, slug)
    return redirect("foodster:menu")

def order_add_to_cart(request, slug):
    base_add_to_cart(request, slug)
    return redirect("foodster:order-summary")

@login_required
def base_remove_whole_item_from_cart(request, slug):
    item = get_object_or_404(FoodDish, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )

    if order_qs.exists():
        order = order_qs[0]

        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.get_or_create(
                    item=item,
                    user=request.user,
                    ordered=False,
                )[0]

            order.items.remove(order_item)
            order_item.delete()
        
            messages.info(request, f"{item.name} remmoved from basket")

        else:
            messages.info(request, f"The order does not have this item")

    else:
        messages.info(request, f"There is no order for this user")

    return redirect("foodster:order-summary")

@login_required
def base_remove_from_cart(request, slug):
    item = get_object_or_404(FoodDish, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )

    if order_qs.exists():
        order = order_qs[0]

        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.get_or_create(
                    item=item,
                    user=request.user,
                    ordered=False,
                )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

            else:
                order.items.remove(order_item)
                order_item.delete()
            
            messages.info(request, f"{item.name} remmoved from basket")

        else:
            messages.info(request, f"The order does not have this item")

    else:
        messages.info(request, f"There is no order for this user")

def remove_from_cart(request, slug):
    base_remove_from_cart(request, slug)
    return redirect("foodster:dish", slug=slug)

def order_remove_from_cart(request, slug):
    base_remove_from_cart(request, slug)
    return redirect("foodster:order-summary")

class FoodDishView(DetailView):
    model = FoodDish
    template_name = "foodster/dish.html"

def place_order(request):
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )

    if order_qs.exists():
        order = order_qs[0]

        order.ordered = True
        order.order_date = timezone.now()
        order.total_price = order.get_total_price()

        for order_item in order.items.all():
            order_item.ordered = True
            order_item.save()

        order.save()
        
    else:
        messages.info(request, f"There is no order for this user")

    messages.info(request, f"Order has been placed")
    return redirect("foodster:homepage")

def account_orders(request):
    user = request.user
    orders = Order.objects.filter(
                    user=request.user, 
                    ordered=True
                    ).order_by("-order_date")

    return render(request, 
                    'foodster/account_orders.html',
                    context={"orders": orders})