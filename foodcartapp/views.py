from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Order, OrderItem


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
def register_order(request):
    orders_info = request.data
    try:
        order = Order.objects.create(
            customer_name=orders_info['firstname'],
            customer_lastname=orders_info['lastname'],
            phone_number=orders_info['phonenumber'],
            address=orders_info['address'],

        )
        if orders_info['products']:
            for item in orders_info['products']:
                OrderItem.objects.get_or_create(
                    order=order,
                    product_id=item['product'],
                    quantity=item['quantity']
                )
        else:
            content = {'error': 'list cannot be empty!'}
            return Response(content, status=status.HTTP_200_OK)

        return Response(orders_info, status=200)
    except TypeError:
        content = {'error': 'invalid data type!'}
        return Response(content, status=status.HTTP_200_OK)
    except KeyError:
        content = {'error': 'required fields not filled!'}
        return Response(content, status=status.HTTP_200_OK)
