import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order


# Create queries within functions
def get_profiles(search_string=None):
    """
            This function accepts the following argument with default None value:
        •	search_string – string value or None
        It retrieves profile objects by partially and case-insensitively matching the given searching criteria
        for full name, email, or phone number.
        Check if any of these three field values (full name, email, or phone number) contain the search string.
        Order the profile objects by full name, ascending.
        Return a string in the following format, each profile info on a new line:
        "Profile: {full_name1}, email: {email1}, phone number: {phone_number1}, orders: {num_of_orders1}
        Profile: {full_name2}, email: {email2}, phone number: {phone_number2}, orders: {num_of_orders2}
        …
        Profile: {full_nameN}, email: {emailN}, phone number: {phone_numberN}, orders: {num_of_ordersN}"
        o	If no profiles match the criteria, return an empty string ("").
        o	Hint: You can use Q objects but first check if the search string is not None.
    """
    if search_string is None:
        return ""

    query = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(
        phone_number__icontains=search_string)

    profiles = Profile.objects.filter(query).annotate(num_of_orders=Count('orders')).order_by('full_name')

    if not profiles.exists():
        return ""

    return '\n'.join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.num_of_orders}"
        for p in profiles)


def get_loyal_profiles():
    """
            This function accepts no arguments.
        It retrieves profile objects with more than two orders, ordered by number of orders, descending.
        You should count all orders regardless of their status ("Completed" or "Not Completed").
        Return a string in the following format, each profile info on a new line:
        "Profile: {full_name1}, orders: {num_of_orders1}
        Profile: {full_name2}, orders: {num_of_orders2}
        …
        Profile: {full_nameN}, orders: {num_of_ordersN}"
        o	If no profiles match the criteria, return an empty string ("").
        o	Hint: You can use the custom model manager method.
    """
    profiles = Profile.objects.get_regular_customers()
    if not profiles.exists():
        return ""

    return '\n'.join(f"Profile: {p.full_name}, orders: {p.num_orders}" for p in profiles)


def get_last_sold_products():
    """
            This function accepts no arguments.
        It retrieves the products from the latest order object, ordered by product name, ascending.
        The status of the order does not matter ("Completed" or "Not Completed").
        Return a string in the following format:
        "Last sold products: {product_name1}, {product_name2}, … {product_nameN}"
        o	Product names must be separated by a comma and space (", ")
        o	If there are no orders and respectively no products sold, return an empty string ("").
    """
    order = Order.objects.prefetch_related('products').order_by('-creation_date').first()

    if not order or not order.products.all().exists():
        return ""

    return f"Last sold products: {', '.join(p.name for p in order.products.all() if p)}"


def get_top_products():
    """
        This function accepts no arguments.
    It retrieves the most frequently sold products from all orders. Order them by the number of times the product has
    been sold (included in an order), descending, then ascending by product name.
    The status of the orders does not matter ("Completed" or "Not Completed").
    Take the top five ordered products.
    Return a string in the following format:
    "Top products:
    {product_name1}, sold {num_orders1} times
    {product_name2}, sold {num_orders2} times
     …
    {product_name5}, sold {num_orders5} times"
    o	Product name and sales info must be separated by a comma and space (", "). Each product info is on a new line.
    o	In case the sold items are less than five in total, return all of them, ordered as described.
    o	If there are no orders and respectively no products sold, return an empty string ("").

    """
    products = Product.objects.annotate(num_orders=Count('orders')).filter(num_orders__gt=0).order_by('-num_orders',
                                                                                                      'name')[:5]

    if not products.exists():
        return ""

    top_products = '\n'.join(f"{p.name}, sold {p.num_orders} times" for p in products)

    return f"Top products:\n{top_products}"


def apply_discounts():
    """
        This function accepts no arguments.
    It retrieves order objects that have more than two products, whose status is "Not Completed" (is_completed=False),
    and applies a discount of 10% to the total price.
    Return a string in the following format:
    "Discount applied to {num_of_updated_orders} orders."
    o	If no orders are affected, the value of "num_of_updated_orders" will be 0 (zero).
    o	Hint: You can use F object to efficiently update the total price for all selected orders.
    """
    query = Q(num_products__gt=2) & Q(is_completed=False)

    num_of_updated_orders = Order.objects.annotate(num_products=Count('products')).filter(query).update(
        total_price=F('total_price') * 0.90
    )

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    """
        This function accepts no arguments.
    It retrieves the first (oldest) order object from your database whose status is "Not Completed" and changes it
    from "Not Completed" (is_completed=False) to "Completed" (is_completed=True).
    Remember that you must decrease the quantity of the ordered products you have in stock (in_stock).
    If a quantity becomes 0 (zero), change the status of the product to "Not Available" (is_available=False).
    Return a string in the following format:
    "Order has been completed!"
    o	If there are no orders or all orders have been completed, return an empty string ("").

    """

    oldest_order = Order.objects.prefetch_related('products').filter(is_completed=False).order_by(
        'creation_date').first()

    if not oldest_order:
        return ""

    for product in oldest_order.products.all():
        product.in_stock -= 1
        product.is_available = False if product.in_stock == 0 else True
        product.save()

    oldest_order.is_completed = True
    oldest_order.save()

    return "Order has been completed!"
