# Generated by Django 5.0.4 on 2024-07-01 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_product_discountedproduct'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DiscountedProduct',
        ),
        migrations.CreateModel(
            name='DiscountedProduct',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_app.product',),
        ),
    ]
