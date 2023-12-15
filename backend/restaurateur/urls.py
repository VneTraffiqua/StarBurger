from django.urls import path
from django.shortcuts import redirect

from .views import view_orders, view_products, view_restaurants, LoginView, LogoutView

app_name = "restaurateur"

urlpatterns = [
    path('', lambda request: redirect('restaurateur:ProductsView')),

    path('products/', view_products, name="ProductsView"),

    path('restaurants/', view_restaurants, name="RestaurantView"),

    # TODO заглушка для нереализованного функционала
    path('orders/', view_orders, name="view_orders"),

    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
