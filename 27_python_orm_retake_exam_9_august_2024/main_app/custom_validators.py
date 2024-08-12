from django.core.exceptions import ValidationError


def code_validator(value):
    if not len(value) == 4:
        raise ValidationError("Code must contain exactly 4 characters")

