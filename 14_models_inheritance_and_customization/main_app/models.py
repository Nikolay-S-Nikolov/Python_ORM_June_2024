from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

# Multi-table Inheritance --------------------------------
"""
Multi-table inheritance creates a separate database table for each model in the inheritance chain.
Each table includes fields from all the parent models in the hierarchy.
Django automatically generates a OneToOneField field for the relationship in the child's model to its parent.


class ParentModel(models.Model):
    parent_field = models.CharField(max_length=50)   # A field that a child will inherit from its paren


class ChildModel(ParentModel):
    child_field = models.IntegerField() # Own field that only child has
"""

# Abstract Base Classes ------------------------------------

"""
Abstract models are base classes. They allow other models to inherit fields and methods from them.
Abstract models do not create their own database tables.
They act as templates for other models to reuse common fields and behavior.


class AbstractBaseModel(models.Model):
    common_field = models.CharField(max_length=100)  # A field that a child will inherit from its paren

    class Meta:
         -Use the inner class Meta to insert metadata into the model.
         -Adding Meta inner class is optional.
    abstract = True  # No database table will be created. Turns the model into an Abstract Base Class.


    class ChildModel(AbstractBaseModel):
        additional_field = models.IntegerField()  # Own field that only child has
"""

# Proxy Models ----------------------------------------------------------------

"""
Proxy models allow you to create a new model that behaves exactly like an existing model with some customizations added.
The proxy model uses the same database table as the original model.
Useful when adding extra methods, managers, or custom behavior to an existing model without modifying the original model

class OriginalModel(models.Model):
    ...
    field = models.CharField(max_length=5)  # Original model fields


class ProxyModel(OriginalModel):
    ...  # Add some extra methods here

    class Meta:
        proxy = True  # No new table will be created
"""

# Model Methods ----------------------------------------------------------------

"""
Model methods are functions defined within a Django model.
They allow you to perform operations on model instances adn other tasks related to the model.
Types of model methods:
- Built-in methods:
    Built-in Methods are standard methods provided by Django's models.Model class.
    Main built-in methods
     - save() - Called when saving an instance to the database
     - clean() - Used for data validation before saving
    Override built-in methods to add custom behavior or validation to a model
    
        class MyModel(models.Model):
            field = models.CharField(max_length=100)
        
            def save(self, *args, **kwargs):
                ...  # Add custom logic before saving here
                super().save(*args, **kwargs)  # Call the original save method
        
            def clean(self):
                ...  # Custom validation logic    
                
- Custom methods
    Additional methods defined in a model performing specific tasks or calculations related to the model
    It is acting on a particular model instance and keeping business logic in one place
        class MyModel(models.Model):
            field = models.CharField(max_length=100)
    
            def custom_method(self): # Custom model method 
                ...  # Custom logic here
"""

# Custom Model Properties

"""
Custom model properties allow you to define new attributes for a model that are not stored in the database and are
calculated or derived from existing model fields. They are similar to regular model fields but do not correspond to 
database columns and are defined as Python class properties.

    from datetime import date

    class Employee(models.Model):
        birth_date = models.DateField()
        ...
    
        @property
        def age(self) -> int:
            days_in_year = 365.2425
            return int((date.today() - self.birth_date).days / days_in_year)
            
The decorator allows you to define a method that acts as a property and does not require a database column.
"""

# Custom Fields

"""
Custom Fields
    Django allows you to create custom fields by subclassing django.db.models.Field or one of the existing field classes
    models.CharField, models.IntegerField, etc.
    Custom fields can be helpful when using custom data type, validation and serialization for your model fields
    
Custom Fields Built-in Methods
    Django provides several built-in custom field methods that you can override to customize the behavior of the
     custom model field.
    Some of the most useful built-in custom field methods are
      - from_db_value() - converts the field's value as retrieved from the database into its Python representation
      - to_python() - converts the field's value from the serialized format (usually as a string) into its Python
       representation
      - get_prep_value() - prepares the field's value before saving it to the database
      - validate() - performs custom validation on the field's value
      - deconstruct() - used when serializing the field to store its constructor arguments as a tuple, allowing 
      Django to recreate the field when migrating or serializing models
      
            class PhoneNumberField(models.CharField):
                def __init__(self, *args, **kwargs):
                    kwargs['max_length'] = 15  # defining max length
                    super().__init__(*args, **kwargs)
            
                def get_prep_value(self, value):  # Preparing value for saving in DB
                    if value is None:
                        return value
                    return ''.join(filter(str.isdigit, value))  # filtering only the digits to be saved in DB
            
            
            class Employee(models.Model):
                ...
                phone_number = models.PhoneNumberField(default='111-111-111')
"""


# 01. Zoo Animals ----------------------------------------------------------------

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    # @property
    # def age(self) -> int:
    #     days_in_year = 365.2425
    #     return int((date.today() - self.birth_date).days / days_in_year)

    @property
    def age(self) -> int:
        today = date.today()
        return (today.year - self.birth_date.year) - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


# 02. Zoo Employees --------------------------------------------------------

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    SPECIALITY_CHOICES = (
        ('Mammals', 'Mammals'),
        ('Birds', 'Birds'),
        ('Reptiles', 'Reptiles'),
        ('Others', 'Others'),
    )
    specialty = models.CharField(max_length=10, choices=SPECIALITY_CHOICES)
    managed_animals = models.ManyToManyField('Animal')

    def clean(self):
        super().clean()
        choices = [choice[0] for choice in self.SPECIALITY_CHOICES]

        if self.specialty not in choices:
            raise ValidationError("Specialty must be a valid choice.")


# class Veterinarian(Employee):
#     license_number = models.CharField(max_length=10)


# 03. Animal Display System ----------------------------------------------------------------

class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    def display_info(self):
        return (f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. "
                f"It makes a noise like '{self.sound}'.")

    def is_endangered(self):
        if self.species in ["Cross River Gorilla", "Orangutan", "Green Turtle"]:
            return f"{self.species} is at risk!"
        return f"{self.species} is not at risk."


# 04. Zookeeper's Specialty ----------------------------------------------------------------
# In the "ZooKeeper" model added custom validation logic
#     def clean(self):
#         choices = [choice[0] for choice in self.SPECIALITY_CHOICES]
#
#         if self.specialty not in choices:
#             raise ValidationError("Specialty must be a valid choice.")


# 05. Animal Display System Logic ----------------------------------------------------------------

# Add the following logic to the "ZooDisplayAnimal" model
#     def display_info(self):
#         return (f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. "
#                 f"It makes a noise like '{self.sound}'.")
#
#     def is_endangered(self):
#         if self.species in ["Cross River Gorilla", "Orangutan", "Green Turtle"]:
#             return f"{self.species} is at risk!"
#         return f"{self.species} is not at risk."


# 06. Animal's Age ----------------------------------------------------------------

# In the "Animal" model implement property that calculates and returns the animal age
#
#             @property
#             def age(self) -> int:
#                 days_in_year = 365.2425
#                 return int((date.today() - self.birth_date).days / days_in_year)

#                 @property
#                     def age(self) -> int:
#                         today = date.today()
#                         return (today.year - self.birth_date.year) - (
#                                     (today.month, today.day) < (self.birth_date.month, self.birth_date.day))


# 07. Veterinarian Availability ----------------------------------------------------------------

class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ((True, "Available"), (False, "Not Available"))
        kwargs['default'] = True
        super().__init__(*args, **kwargs)


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()
