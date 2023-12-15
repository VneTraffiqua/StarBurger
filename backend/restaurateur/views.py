from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from foodcartapp.models import Order, Product, Restaurant
from geopy.distance import distance
from operator import itemgetter
from places import models


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    addresses = models.Place.objects.all()
    orders = Order.objects.get_order_params().get_order_value().filter(
            status__in=('Необработан', 'Готовится')
        ).order_by('-id')

    for order in orders:
        restaurants = []
        restaurants_coordinates = {}

        for product in order.order_products:
            rest_list = []

            for rest in product.product.rests: # Finding which restaurant can cook the product
                if rest.availability:
                    rest_list.append(rest.restaurant.name)
                    restaurants_coordinates[rest.restaurant.name] = (rest.restaurant.lat, rest.restaurant.lon)
            restaurants.append(set(rest_list))

        order_rest = restaurants[0]  # Determine the restaurant that will be can cook to prepare the entire order
        for rest in restaurants:
            order_rest = order_rest.intersection(rest)
        order.rest = list(order_rest)

        restaurants_distance = {}  # Determine the distance to each restaurant
        for rest in list(order_rest):
            restaurants_distance[rest] = restaurants_coordinates.pop(rest)
        for rest in restaurants_distance.keys():
            for place in addresses:
                if order.address == place.address:
                    restaurants_distance[rest] = distance(
                        (place.lat, place.lon),
                        restaurants_distance[rest]
                    ).km
        order.rest = dict(sorted(restaurants_distance.items(), key=itemgetter(1)))

        if order.status == 'Необработан' and order.order_restaurant:  # Changed order status when a restaurant is selected
            order.status = 'Готовится'
            order.save()
    return render(request, template_name='order_items.html', context={
        'order_items': orders,
        'currentUrl': request.path
    })
