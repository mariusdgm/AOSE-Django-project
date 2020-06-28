"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "foodster"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("menu/", views.menu, name="menu"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("order-summary/", views.OrderSummaryView.as_view(), name="order-summary"),
    path("dish/<slug>/", views.FoodDishView.as_view() , name="dish"),
    path("add-to-cart/<slug>/", views.add_to_cart, name="add-to-cart"),
    path("quick-add-to-cart/<slug>/", views.quick_add_to_cart, name="quick-add-to-cart"),
    path("order-add-to-cart/<slug>/", views.order_add_to_cart, name="order-add-to-cart"),
    path("order-remove-from-cart/<slug>/", views.order_remove_from_cart, name="order-remove-from-cart"),
    path("order-remove-from-cart-whole-item/<slug>/", views.base_remove_whole_item_from_cart, name="order-remove-from-cart-whole-item"),
    path("remove-from-cart/<slug>/", views.remove_from_cart, name="remove-from-cart"),
    path("place-order/", views.place_order, name="place-order"),
    path("account-orders/", views.account_orders, name="account-orders"),
]
