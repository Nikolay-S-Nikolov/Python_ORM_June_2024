# Generated by Django 5.0.4 on 2024-06-19 19:11

from django.db import migrations


def set_price(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    smartphones = smartphone_model.objects.all()

    for smartphone_record in smartphones:
        smartphone_record.price = len(smartphone_record.brand) * 120
        smartphone_record.save()

    # smartphone_model.objects.bulk_update(smartphones, ['price'])


def set_category(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    smartphones = smartphone_model.objects.all()

    for smartphone_records in smartphones:
        if smartphone_records.price > 751:
            smartphone_records.category = 'Expensive'
        else:
            smartphone_records.category = 'Cheap'
        smartphone_records.save()


def set_category_and_price(apps, schema_editor):
    set_price(apps, schema_editor)
    set_category(apps, schema_editor)


def revers_code(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')
    default_category = smartphone_model._meta.get_field('category').default

    for smartphone in smartphone_model.objects.all():
        smartphone.price = 0
        smartphone.category = default_category
        smartphone.save()


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0013_smartphone'),
    ]

    operations = [migrations.RunPython(set_category_and_price, reverse_code=revers_code)
                  ]
