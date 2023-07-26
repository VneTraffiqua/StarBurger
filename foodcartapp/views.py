from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .models import Product, Order, OrderItem
from .serializers import OrderSerializer
from places import places_coord
from environs import Env


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([ 
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
@transaction.atomic
def register_order(request):
    env = Env()
    env.read_env()
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    lat, lon = places_coord.add_place(serializer.validated_data['address'])
    order = Order.objects.create(
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        phonenumber=serializer.validated_data['phonenumber'],
        address=serializer.validated_data['address'],
        lat=lat,
        lon=lon

    )
    products_fields = serializer.validated_data['products']
    products = [
        OrderItem(order=order, **products) for products in products_fields
    ]
    for product in products:
        product.price = product.product.price

    OrderItem.objects.bulk_create(products)

    return Response(serializer.data)

