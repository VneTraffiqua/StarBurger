# Generated by Django 3.2.15 on 2023-03-02 09:19

from django.db import migrations


def create_price_at_order_items(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for item in OrderItem.objects.all():
        item.price = None
        OrderItem.objects.update_or_create(price=item.product.price)


def move_backward(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for item in OrderItem.objects.all():
        item.price = None
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_auto_20230302_0919'),
    ]

    operations = [
        migrations.RunPython(create_price_at_order_items, move_backward)
    ]
