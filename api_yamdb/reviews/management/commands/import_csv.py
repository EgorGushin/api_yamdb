import sqlite3

import pandas as pd
from django.core.management.base import BaseCommand


# from reviews.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        con = sqlite3.connect('db.sqlite3')

        cat_dt = pd.read_csv('static/data/category.csv', sep=',')
        com_dt = pd.read_csv('static/data/comments.csv', sep=',')
        gen_dt = pd.read_csv('static/data/genre.csv', sep=',')
        gen_titl_dt = pd.read_csv('static/data/genre_title.csv', sep=',')
        rev_dt = pd.read_csv('static/data/review.csv', sep=',')
        titl_dt = pd.read_csv('static/data/titles.csv', sep=',')
        # usrs_dt = pd.read_csv('static/data/users.csv', sep=',')
        # print(usrs_dt)
        cat_dt.to_sql(
            'reviews_category', con, if_exists='replace', index=False
        )
        com_dt.to_sql('reviews_comment', con, if_exists='replace', index=False)
        gen_dt.to_sql('reviews_genre', con, if_exists='replace', index=False)
        gen_titl_dt.to_sql(
            'reviews_genretitle', con, if_exists='replace', index=False
        )
        rev_dt.to_sql('reviews_review', con, if_exists='replace', index=False)
        titl_dt.to_sql('reviews_title', con, if_exists='replace', index=False)
        # usrs_dt.to_sql('reviews_user', con, if_exists='replace', index=False)
        # users = [
        #     User(
        #         id=row.get('id'),
        #         username=row.get('username'),
        #         email=row.get('email'),
        #         role=row.get('role'),
        #         bio=row.get('bio'),
        #         first_name=row.get('first_name'),
        #         last_name=row.get('last_name'),
        #         password=row.get('password')
        #     ) for i, row in usrs_dt.iterrows()
        # ]
        # User.objects.all().delete()
        # User.objects.bulk_create(users)
        print('Данные записаны в БД')
