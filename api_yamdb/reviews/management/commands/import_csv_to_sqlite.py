import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Review, Comment, Category, Genre, Title, User


TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    # GenreTitle: 'genre_title.csv'
}


class Command(BaseCommand):
    help = 'Load csv data'

    def handle(self, *args, **kwargs):
        for model, data in TABLES.items():
            with open(
                    f'{settings.BASE_DIR}/static/data/{data}',
                    'r',
                    encoding='UTF-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Successfully'))
