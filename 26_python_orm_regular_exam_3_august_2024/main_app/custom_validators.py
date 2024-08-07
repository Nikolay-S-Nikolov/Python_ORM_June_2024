from django.core.exceptions import ValidationError


def only_digit_validator(value):
    if not value.isdigit():
        raise ValidationError('Must contain only digits')
