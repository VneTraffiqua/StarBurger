s[0].products.all()[0].product.price * s[0].products.all()[0].quantity
s = models.Order.objects.all()
for item in s:
    for product in item.products.all():
        product.product.price * product.quantity