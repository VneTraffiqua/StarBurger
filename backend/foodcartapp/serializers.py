from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    price = IntegerField(required=False)
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'address',
            'products'
        ]

