from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError(
            f'Год произведения не может быть больше, чем {current_year}!'
        )
