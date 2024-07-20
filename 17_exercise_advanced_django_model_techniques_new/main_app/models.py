from django.contrib.postgres.search import SearchVectorField
from django.core.validators import RegexValidator, MinValueValidator, MinLengthValidator
from django.db import models
from decimal import Decimal


# 01. Customer-----------------------------------------------------------------------------

class Customer(models.Model):
    name = models.CharField(max_length=100, validators=[
        RegexValidator(
            r'^[A-Za-z\s]*$',  # alternative regex r'[^A-Z,a-z,\s]' but with inverse_match=True
            "Name can only contain letters and spaces",
        )])

    age = models.PositiveIntegerField(
        validators=[MinValueValidator(
            18,
            "Age must be greater than or equal to 18"
        )])

    email = models.EmailField(
        error_messages={'invalid': "Enter a valid email address"},
    )

    phone_number = models.CharField(
        max_length=13,
        validators=[RegexValidator(
            r'^\+359\d{9}$',
            "Phone number must start with '+359' followed by 9 digits"
        )]
    )

    website_url = models.URLField(
        error_messages={'invalid': "Enter a valid URL"},
    )


# 02. Media -----------------------------------------------------------------------------

class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']


class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(
            5,
            "Author must be at least 5 characters long")]
    )

    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(
            6,
            'ISBN must be at least 6 characters long'
        )]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"


class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(
            8,
            "Director must be at least 8 characters long",
        )]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"


class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(
            9,
            "Artist must be at least 9 characters long"
        )]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"


# 03. Tax-Inclusive Pricing ----------------------------------------------------------------

class Product(models.Model):
    TAX_RATE = 8
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self):
        return self.price * self.TAX_RATE / 100

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * 2

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    TAX_RATE = 5

    def calculate_price_without_discount(self):
        return self.price + self.price * 20 / 100

    def calculate_tax(self):
        return self.price * self.TAX_RATE / 100

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * Decimal(1.5)

    def format_product_name(self):
        return f"Discounted Product: {self.name}"


# 04. Superhero Universe ----------------------------------------------------------------
class RechargeEnergyMixin(models.Model):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def recharge_energy(self, amount: int):
        self.energy = min(100, self.energy + amount)
        self.save()


class Hero(RechargeEnergyMixin):
    pass


class SpiderHero(Hero):
    class Meta:
        proxy = True

    def swing_from_buildings(self):
        if self.energy < 80:
            return f"{self.name} as Spider Hero is out of web shooter fluid"
        self.energy -= 80
        if self.energy == 0:
            self.energy = 1
        self.save()
        return f"{self.name} as Spider Hero swings from buildings using web shooters"


class FlashHero(Hero):
    class Meta:
        proxy = True

    def run_at_super_speed(self):
        if self.energy < 65:
            return f"{self.name} as Flash Hero needs to recharge the speed force"
        self.energy -= 65
        if self.energy == 0:
            self.energy = 1
        self.save()
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"


# 05 Vector Searching ----------------------------------------------------------------

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['search_vector'])
        ]
