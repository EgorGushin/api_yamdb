from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Использовать никнейм "me" запрещено.'
        )


def valid_year(value):
    if value > timezone.now().year:
        raise ValidationError('Введенный год не может быть больше текущего.')
