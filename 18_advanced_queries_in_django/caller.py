import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct, product_quantity_ordered, \
    ordered_products_per_customer, filter_products, give_discount


# Create and run queries
def add_records_to_database():
    # Categories
    food_category = Category.objects.create(name='Food')
    drinks_category = (Category.objects.create(name='Drinks'))

    # Food
    product1 = Product.objects.create(name='Pizza', description='Delicious pizza with toppings', price=10.99,
                                      category=food_category, is_available=False)
    product2 = Product.objects.create(name='Burger', description='Classic burger with cheese and fries', price=7.99,
                                      category=food_category, is_available=False)
    product3 = Product.objects.create(name='Apples', description='A bag of juicy red apples', price=3.99,
                                      category=food_category, is_available=True)
    product4 = Product.objects.create(name='Bread', description='A freshly baked loaf of bread', price=2.49,
                                      category=food_category, is_available=True)
    product5 = Product.objects.create(name='Pasta and Sauce Bundle',
                                      description='Package containing pasta and a jar of pasta sauce', price=6.99,
                                      category=food_category, is_available=False)
    product6 = Product.objects.create(name='Tomatoes', description='A bundle of ripe, red tomatoes', price=2.99,
                                      category=food_category, is_available=True)
    product7 = Product.objects.create(name='Carton of Eggs', description='A carton containing a dozen fresh eggs',
                                      price=3.49, category=food_category, is_available=True)
    product8 = Product.objects.create(name='Cheddar Cheese', description='A block of aged cheddar cheese', price=7.99,
                                      category=food_category, is_available=False)
    product9 = Product.objects.create(name='Milk', description='A gallon of fresh cow milk', price=3.49,
                                      category=food_category, is_available=True)

    # Drinks
    product10 = Product.objects.create(name='Coca Cola', description='Refreshing cola drink', price=1.99,
                                       category=drinks_category, is_available=True)
    product11 = Product.objects.create(name='Orange Juice', description='Freshly squeezed orange juice', price=2.49,
                                       category=drinks_category, is_available=False)
    product12 = Product.objects.create(name='Bottled Water', description='A 12-pack of purified bottled water',
                                       price=4.99, category=drinks_category, is_available=True)
    product13 = Product.objects.create(name='Orange Soda', description='A 6-pack of carbonated orange soda', price=5.49,
                                       category=drinks_category, is_available=True)
    product14 = Product.objects.create(name='Bottled Green Tea', description='A bottled green tea', price=3.99,
                                       category=drinks_category, is_available=False)
    product15 = Product.objects.create(name='Beer', description='A bottled craft beer', price=5.49,
                                       category=drinks_category, is_available=True)

    # Customers
    customer1 = Customer.objects.create(username='john_doe')
    customer2 = Customer.objects.create(username='alex_alex')
    customer3 = Customer.objects.create(username='peter132')
    customer4 = Customer.objects.create(username='k.k.')
    customer5 = Customer.objects.create(username='peter_smith')

    # Orders
    order1 = Order.objects.create(customer=customer1)
    order_product1 = OrderProduct.objects.create(order=order1, product=product3, quantity=2)
    order_product2 = OrderProduct.objects.create(order=order1, product=product6, quantity=1)
    order_product3 = OrderProduct.objects.create(order=order1, product=product7, quantity=5)
    order_product4 = OrderProduct.objects.create(order=order1, product=product13, quantity=1)

    order2 = Order.objects.create(customer=customer3)
    order_product5 = OrderProduct.objects.create(order=order2, product=product3, quantity=2)
    order_product6 = OrderProduct.objects.create(order=order2, product=product9, quantity=1)

    order3 = Order.objects.create(customer=customer1)
    order_product5 = OrderProduct.objects.create(order=order3, product=product12, quantity=4)
    order_product6 = OrderProduct.objects.create(order=order3, product=product7, quantity=3)
    return "All data entered!"


# Run and print your queries
# print(add_records_to_database())

# 01. Available Products ----------------------------------------------------

"""
In Django, a manager is an interface through which database query operations are performed.
By default, Django provides a manager called objects for every model.
You can create custom managers to encapsulate specific query logic and make it reusable throughout your application.
Custom managers are useful when you want to add custom methods and filters to retrieve data from the database
They allow you to define specialized query sets tailored to your application's needs.
To create a custom manager, you need to subclass models.Manager and define your custom methods there

"""
#
# print('All Products:')
# print(Product.objects.all())
# print()
# print('All Available Products:')
# print(Product.objects.available_products())
# print()
# print('All Available Food Products:')
# print(Product.objects.available_products_in_category("Food"))


# 02. Product Quantity Ordered----------------------------------------------------

"""
Annotation
Annotation in Django is a powerful feature that allows you to add calculated fields to your query results.
The annotate() method is used to add the calculated fields to the queryset.
Annotation can be useful when you need to perform aggregation or add derived values to your model instances.
 Annotation is a powerful tool that 
    - extends your query capabilities
    - allows you to retrieve aggregated or calculated data efficiently
    - keeps your model structure clean
    - separates model structure from the query logic
"""
# print(product_quantity_ordered())


# 03. Ordered Products Per Customer -------------------------------------------------


"""
Queries for Model Relationships
Specific methods are used to optimize database queries
     - When dealing with related objects in your models
     - Helping to reduce the number of queries executed
     - Improving performance
 - select_related() - Used to optimize queries involving ForeignKey and OneToOneField relationships
         -  It fetches related objects in the same query rather than executing a separate query for each 
         related object
         - Significantly reduces the number of database queries and improves performance
         
 - prefetch_related() - Used for optimizing queries involving ManyToManyField, reverse ForeignKey, and 
 reverse OneToOneField relationships
         - It fetches related objects in a separate query and caches them for efficient lookup
         - Helps to avoid the N+1 query problem, where N is the number of objects being queried
"""

print(ordered_products_per_customer())

# 04. Available Products Prices ------------------------------------------------

# print(filter_products())

# 05. Give Discounts ------------------------------------------------

# print(give_discount())
