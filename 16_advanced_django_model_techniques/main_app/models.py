from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


# 06. Rating and Review Content -------------------------------------------------

class ReviewMixin(models.Model):
    review_content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)]
    )

    class Meta:
        abstract = True
        ordering = ['-rating']


# Built-in Field Validators ------------------------------------------------

class Employee(models.Model):
    """
    Django provides built-in field validators allowing to validate the data entered in the model fields
     and ensure that the data meets specific requirements before saving it.
        - Common built-in validators
            MaxValueValidator, MinValueValidator
            MaxLengthValidator, MinLengthValidator
            RegexValidator
     Min/Max Length/Value Validators accept two arguments
        - limit_value -  A required, first positional argument that specifies the limit value
        - message - A default argument message=None is being passed by default
     Validators raise a ValidationError if the field value does not meet the requirements
     "validators" option is used to apply a list of validators to a specific field
    """

    first_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, message='First name should be at least 2 chars long')],
    )  # Validators can be passed as a list or tuple. Message is None by default


# 01. Restaurant ----------------------------------------------------------------

class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, "Name must be at least 2 characters long."),
            MaxLengthValidator(100, "Name cannot exceed 100 characters.")
        ]
    )
    location = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2, "Location must be at least 2 characters long."),
            MaxLengthValidator(200, "Location cannot exceed 200 characters.")

        ]
    )
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00, "Rating must be at least 0.00."),
            MaxValueValidator(5.00, "Rating cannot exceed 5.00.")
        ]
    )


# Custom Validators
def validate_even(value):  # Custom function that accepts the field value

    """
     Create custom validators when you need to implement a custom validation logic
        - How to create a custom validator
            Define a function that takes the field's value applies some validation logic and  raises a ValidationError
            if the value does not meet the requirements.
    """

    if value % 2 != 0:  # custom validation logic
        raise ValidationError('Value must be an even number!')  # raise a ValidationError with error message


class MyModel(models.Model):
    number = models.IntegerField(
        validators=[validate_even]  # used custom validator validate_even
    )


# 02. Menu --------------------------------------------------------------------------------
# import re
def validate_menu_categories(value: str) -> None:
    # if not len([x for x in ["Appetizers", "Main Course", "Desserts"] if re.search(x, value)]) == 3:
    if not all(value.__contains__(x) for x in ["Appetizers", "Main Course", "Desserts"]):
        raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(validators=[validate_menu_categories])
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE
    )


# Meta Class and Meta Options
class MyMetaOptionsModel(models.Model):
    """
    Metaclass allows you to provide additional information about a model
     Used to specify model-level options like:
        - abstract - If True, indicates that the model will be an Abstract Base Class
        - proxy - If True, indicates that the model will be a Proxy Model
        - db_table - Overrides the default database table name for the model
        - ordering - Defines a default order when a collection of model objects is obtained
        - unique_together - Defines a set of field names that their values together must be unique
        - constraints - list of constraints that you want to define on the model
        - verbose_name - Defines a human-readable name for the object (singular)
        - verbose_name_plural - Defines a plural name for the object. By default, Django uses the model
        or verbose name (if given) + "s"
    """
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        db_table = 'custom_table_name'  # Defines a custom name for the database table
        ordering = ('-name', 'id')  # defines default object ordering
        unique_together = ('name', 'id')  # Defines a unique constraint.
        # A unique constraint will be applied to the combination of "name" and "id" fields
        constraints = [models.CheckConstraint(
            check=models.Q(age__gte=18),
            name="age_gte_18",
            violation_error_message='Age must be at least 18'
        )]


# 03. Restaurant Review ----------------------------------------------------------------

class RestaurantReview(ReviewMixin):
    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE
    )

    class Meta(ReviewMixin.Meta):
        abstract = True  # changed to abstract as requested in Problem 04. Restaurant Review Types
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ['reviewer_name', 'restaurant']


# Meta Inheritance ----------------------------------------------------------------
class BaseAbstractModel(models.Model):
    """
    When you create a child model that inherits from an abstract model it can also define its own Meta class.
    Own Meta class completely overrides the parent's one unless it extends it by subclassing.
    If the child model does not have its own Meta class Django will look for the Meta class in the parent
    abstract model and inherit its options.
    """
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ['name']


class ChildModel(BaseAbstractModel):
    description = models.TextField()
    """
    class Meta:             # Child's Meta class overrides parent the inherited parent's one.
        verbose_name_plural = 'Child Models'
        ordering = ['name']
    """

    class Meta(BaseAbstractModel.Meta):  # Child's Meta class extends the parent's one by subclassing it
        verbose_name_plural = 'Child Models'


# 04. Restaurant Review Types ------------------------------------------------------------

class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)

    class Meta(RestaurantReview.Meta):
        """
        Meta Inheritance is possible only if the parent is an abstract base class.
        If the child defines its own Meta class, it overrides the inherited one from the abstract parent unless
        it extends the parent's Meta class by subclassing it.
        When a model inherits from a non-abstract parent with а Meta class, the child's Meta class is independent, and
        it will not inherit or be affected by the Meta options of the parent model
        """
        verbose_name = "Food Critic Review"
        verbose_name_plural = "Food Critic Reviews"


# Indexing in Models -----------------------------------------------------------------------------

class MyModelIndexingExample(models.Model):
    """
     In Django models, indexing is used to optimize database queries for specific fields by adding an index
      to a field, you can speed up search operations on that field.
      Database uses indexes to locate rows much faster significantly reducing the time to retrieve the data.
      By default, the database creates an index for the primary key.
      It is possible to specify additional indexes manually on other fields by using the db_index attribute
      or Meta class option indexes.
    """
    # title = models.CharField(max_length=20, db_index=True)  # additional index on a field
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=100)
    # publication_date = models.DateField(db_index=True)  # additional index on a field
    publication_date = models.DateField()
    genre = models.CharField(max_length=50)

    class Meta:  # Meat option for indexes
        indexes = [  # list of indexes to define
            models.Index(fields=['title', 'author']),  # composite index on both fields
            models.Index(fields=['publication_date']),  # single field index
        ]


# 05. Menu Review --------------------------------------------------------------------------------

class MenuReview(ReviewMixin):
    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(to=Menu, on_delete=models.CASCADE)

    class Meta(ReviewMixin.Meta):
        verbose_name = 'Menu Review'
        verbose_name_plural = 'Menu Reviews'
        unique_together = ["reviewer_name", "menu"]
        indexes = [
            models.Index(fields=['menu'], name="main_app_menu_review_menu_id")
        ]
