import sqlite3

import pandas as pd
from django.core.management.base import BaseCommand


from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_dt = pd.read_csv('static/data/users.csv', sep=',')
        users = [
            User(
                id=row.get('id'),
                username=row.get('username'),
                email=row.get('email'),
                role=row.get('role'),
                bio=row.get('bio'),
                first_name=row.get('first_name'),
                last_name=row.get('last_name'),
                password=row.get('password', i),
                last_login=row.get('last_login'),
                is_superuser=row.get('is_superuser', False),
                is_active=row.get('is_active', False),
                is_staff=row.get('is_staff', False),
                date_joined=row.get(
                    'date_joined',
                    '2011-11-04 00:05:23.283+00:00'),
            ) for i, row in users_dt.iterrows()
        ]
        User.objects.all().delete()
        User.objects.bulk_create(users)

        category_dt = pd.read_csv('static/data/category.csv', sep=',')
        category_db = [
            Category(
                id=row.get('id'),
                name=row.get('name'),
                slug=row.get('slug')
            ) for i, row in category_dt.iterrows()
        ]
        Category.objects.all().delete()
        Category.objects.bulk_create(category_db)

        genre_dt = pd.read_csv('static/data/genre.csv', sep=',')
        genre_db = [
            Genre(
                id=row.get('id'),
                name=row.get('name'),
                slug=row.get('slug')
            ) for i, row in genre_dt.iterrows()
        ]
        Genre.objects.all().delete()
        Genre.objects.bulk_create(genre_db)

        title_dt = pd.read_csv('static/data/titles.csv', sep=',')
        title_db = [
            Title(
                id=row.get('id'),
                name=row.get('name'),
                year=row.get('year'),
                category=Category.objects.get(pk=row.get('category')),
                rating=row.get('rating'),
                description=row.get('description')
            ) for i, row in title_dt.iterrows()
        ]
        Title.objects.all().delete()
        Title.objects.bulk_create(title_db)

        genre_title_dt = pd.read_csv('static/data/genre_title.csv', sep=',')
        genre_title_db = [
            GenreTitle(
                id=row.get('id'),
                title=Title.objects.get(id=row.get('title_id')),
                genre=Genre.objects.get(id=row.get('genre_id'))
            ) for i, row in genre_title_dt.iterrows()
        ]
        GenreTitle.objects.all().delete()
        GenreTitle.objects.bulk_create(genre_title_db)

        review_dt = pd.read_csv('static/data/review.csv', sep=',')
        review_db = [
            Review(
                id=row.get('id'),
                title=Title.objects.get(pk=row.get('title_id')),
                text=row.get('text'),
                author=User.objects.get(pk=row.get('author')),
                score=row.get('score'),
                pub_date=row.get('pub_date')
            ) for i, row in review_dt.iterrows()
        ]
        Review.objects.all().delete()
        Review.objects.bulk_create(review_db)

        comment_dt = pd.read_csv('static/data/comments.csv', sep=',')
        comment_db = [
            Comment(
                id=row.get('id'),
                review=Review.objects.get(id=row.get('review_id')),
                text=row.get('text'),
                author=User.objects.get(id=row.get('author')),
                pub_date=row.get('pub_date')
            ) for i, row in comment_dt.iterrows()
        ]
        Comment.objects.all().delete()
        Comment.objects.bulk_create(comment_db)

        print('Данные записаны в БД')
