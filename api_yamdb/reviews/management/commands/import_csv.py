import csv

from django.core.management.base import BaseCommand

from api_yamdb.settings import STATICFILES_DIRS
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


DATAFILES_DIR = STATICFILES_DIRS
DICT_MODELS_REWIEWS = {
    Category: STATICFILES_DIRS / 'data/category.csv',
    Genre: STATICFILES_DIRS / 'data/genre.csv',
    User: STATICFILES_DIRS / 'data/users.csv',
    Title: STATICFILES_DIRS / 'titles.csv',
    Review: STATICFILES_DIRS / 'data/review.csv',
    Comment: STATICFILES_DIRS / 'data/comments.csv',
    GenreTitle: STATICFILES_DIRS / 'data/genre_title.csv',
}


class Command(BaseCommand):
    help = 'Заполняет базу данных данными из CSV-файлов'

    def handle(self, *args, **options):
        for key, value in DICT_MODELS_REWIEWS.items():
            csv_file = value

            try:
                model = key
            except NameError:
                self.stdout.write(self.style.ERROR('Модель не найдена'))
                return

            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                model.objects.bulk_create(model(**row) for row in reader)

            self.stdout.write(self.style.SUCCESS(
                f'Данные из {csv_file} успешно загружены в базу данных'
            ))

        self.stdout.write(self.style.SUCCESS(
            'Все данные успешно загружены в базу данных!'
        ))
