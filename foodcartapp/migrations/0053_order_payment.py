# Generated by Django 3.2.15 on 2023-03-06 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_alter_order_registered_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Наличностью', 'Наличностью'), ('Электронно', 'Электронно')], db_index=True, default='Наличностью', max_length=15, verbose_name='Способ оплаты'),
        ),
    ]
