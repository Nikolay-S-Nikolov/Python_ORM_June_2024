from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.custom_model_managers import AuthorManager


# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2005)]
    )
    website = models.URLField(blank=True, null=True)
    objects = AuthorManager()

    def __str__(self):
        return self.full_name


class Article(models.Model):
    CATEGORIES = [
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Education', 'Education'),
    ]
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    category = models.CharField(max_length=10, choices=CATEGORIES, default='Technology')
    authors = models.ManyToManyField('Author', related_name='articles')
    published_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title


class Review(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    author = models.ForeignKey('Author', related_name='reviews', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', related_name='reviews', on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True, editable=False)
