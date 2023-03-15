from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class OrderQuerySet(models.QuerySet):
    def get_order_value(self):
        orders = self.annotate(total_sum=models.Sum(
            models.F('products__quantity') * models.F('products__price')
        ))
        return orders


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    lat = models.FloatField(verbose_name='Широта', default=37.617698)
    lon = models.FloatField(verbose_name='Долгота', default=55.755864)
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=500,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    CHOICES = (
        ('Обработан', 'Обработан'),
        ('Необработан', 'Необработан'),
        ('Готовится', 'Готовится')
    )
    status = models.CharField(
        'Статус',
        choices=CHOICES,
        default='Необработан',
        max_length=15,
        db_index=True
    )
    PAYMENT_METHOD = (
        ('Наличностью', 'Наличностью'), ('Электронно', 'Электронно')
    )
    payment = models.CharField(
        'Способ оплаты',
        choices=PAYMENT_METHOD,
        max_length=15,
        db_index=True
    )
    firstname = models.CharField(
        'Имя',
        max_length=50,
        null=False
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=50,
        null=False
    )
    phonenumber = PhoneNumberField(
        'Номер владельца',
        max_length=20,
        region='RU',
        null=False
    )
    address = models.CharField(
        'Адрес', max_length=200,
        null=False
    )
    lat = models.FloatField(verbose_name='Широта', null=True)
    lon = models.FloatField(verbose_name='Долгота', null=True)
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='restaurant',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    comment = models.CharField(
        'Комментарий',
        max_length=200,
        blank=True,
        default=''
    )
    registered_at = models.DateTimeField(
        'Зарегистрирован',
        default=timezone.now,
        db_index=True
    )
    calleded_at = models.DateTimeField(
        'Звонили',
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        'Начали готовить',
        blank=True,
        null=True
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname}, {self.phonenumber} - {self.address}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='products',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=6,
        decimal_places=2,
        null=True,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.product.name
