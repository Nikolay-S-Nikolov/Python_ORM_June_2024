from django.db import models
from django.db.models import Sum, Q, F


# 01. Available Products ----------------------------------------------------

class ProductManager(models.Manager):

    def available_products(self):
        return self.filter(is_available=True)

    def available_products_in_category(self, category_name: str):
        return self.filter(is_available=True, category__name=category_name)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return f"{self.category.name}: {self.name}"


class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


# 02. Product Quantity Ordered----------------------------------------------------
# First variant
# def product_quantity_ordered():
#     qty_ordered = OrderProduct.objects.values('product__name').annotate(
#         quantity_ordered=Sum('quantity')).order_by('-quantity_ordered', 'product_id')
#
#     result = [f"Quantity ordered of {ordered['product__name']}: {ordered['quantity_ordered']}" for ordered in
#               qty_ordered]
#     return '\n'.join(result)


# Second variant
def product_quantity_ordered():
    qty_ordered = Product.objects.filter(order__isnull=False).annotate(
        quantity_ordered=Sum('orderproduct__quantity')).order_by('-quantity_ordered')

    result = [f"Quantity ordered of {product.name}: {product.quantity_ordered}" for product in
              qty_ordered]

    return '\n'.join(result)


# 03. Ordered Products Per Customer -------------------------------------------------

def ordered_products_per_customer():
    ordered_products = Order.objects.prefetch_related('orderproduct_set__product__category').all().order_by('pk')
    result = []
    for order in ordered_products:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        for order_product in order.orderproduct_set.all():
            result.append(f'- Product: {order_product.product.name}, Category: {order_product.product.category.name}')
    return '\n'.join(result)

# 04. Available Products Prices ------------------------------------------------
def filter_products():
    products = Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00)).order_by('-price', 'name')
    result = [f'{product.name}: {product.price}lv.' for product in products]
    return '\n'.join(result)


# 05. Give Discounts ------------------------------------------------

def give_discount():
    Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00)).update(price=F('price') * 0.7)
    products = Product.objects.filter(is_available=True).order_by('-price', 'name')
    result = [f'{product.name}: {product.price}lv.' for product in products]
    return '\n'.join(result)
