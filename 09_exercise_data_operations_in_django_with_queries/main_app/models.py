from django.db import models


# Create your models here.
# 01. Pet ----------------------------------------------------------------
class Pet(models.Model):
    name = models.CharField(max_length=40)
    species = models.CharField(max_length=40)


# 02. Artifact ----------------------------------------------------------------
class Artifact(models.Model):
    name = models.CharField(max_length=70)
    origin = models.CharField(max_length=70)
    age = models.PositiveIntegerField()
    description = models.TextField()
    is_magical = models.BooleanField(default=False)


# 03. Location ----------------------------------------------------------------
class Location(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    population = models.PositiveIntegerField()
    description = models.TextField()
    is_capital = models.BooleanField(default=False)


# 04. Car ----------------------------------------------------------------
class Car(models.Model):
    model = models.CharField(max_length=40)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


# 05. Task Encoder ----------------------------------------------------------------
class Task(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    due_date = models.DateField()
    is_finished = models.BooleanField(default=False)


# 06. Hotel Room ----------------------------------------------------------------
class HotelRoom(models.Model):
    ROOMS = (
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite')
    )
    room_number = models.PositiveIntegerField()
    room_type = models.CharField(max_length=10, choices=ROOMS)
    capacity = models.PositiveIntegerField()
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f'Deluxe room with number {self.room_number} costs {self.price_per_night}$ per night!'


# 07. Character ----------------------------------------------------------------
class Character(models.Model):
    CLASS_NAME_CHOICES = (
        ('Mage', 'Mage'),
        ('Warrior', 'Warrior'),
        ('Assassin', 'Assassin'),
        ('Scout', 'Scout'),
    )
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=20, choices=CLASS_NAME_CHOICES)
    level = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    dexterity = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    hit_points = models.PositiveIntegerField()
    inventory = models.TextField()


















