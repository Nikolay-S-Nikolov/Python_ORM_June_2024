# Generated by Django 5.0.4 on 2024-06-30 13:39

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_mymetaoptionsmodel_restaurantreview_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Child Models',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='RestaurantReview',
            new_name='RegularRestaurantReview',
        ),
        migrations.CreateModel(
            name='FoodCriticRestaurantReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_name', models.CharField(max_length=100)),
                ('review_content', models.TextField()),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('food_critic_cuisine_area', models.CharField(max_length=100)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.restaurant')),
            ],
            options={
                'verbose_name': 'Food Critic Review',
                'verbose_name_plural': 'Food Critic Reviews',
                'ordering': ['-rating'],
                'unique_together': {('reviewer_name', 'restaurant')},
            },
        ),
    ]
