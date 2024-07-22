from django.core.exceptions import ValidationError


# 02. Video Games Library ----------------------------------------------------------------
def validate_value_between_0_and_10(value):
    if not 0.0 <= value <= 10.0:
        raise ValidationError("The rating must be between 0.0 and 10.0")


def validate_value_between_1990_and_2023(value):
    if not 1990 <= value <= 2023:
        raise ValidationError("The release year must be between 1990 and 2023")
