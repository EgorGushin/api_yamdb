from django.core.exceptions import ValidationError
from django.utils import timezone


def valid_year(value):
    if value > timezone.now().year:
        raise ValidationError('Введенный год не может быть больше текущего')