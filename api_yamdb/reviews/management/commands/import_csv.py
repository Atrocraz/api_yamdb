import csv
from django.core.management.base import BaseCommand

from reviews.models import (Category, Title, Genre, User,
                            Review, Comment, TitleGenre)


DICT_MODELS_REWIEWS = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    User: 'static/data/users.csv',
    Title: 'static/data/titles.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
    TitleGenre: 'static/data/genre_title.csv',
}


class Command(BaseCommand):
    help = 'Заполняет базу данных данными из CSV-файлов'

    def handle(self, *args, **options):
        for key, value in DICT_MODELS_REWIEWS.items():
            csv_file = value

            # Получаем модель
            try:
                model = key
            except NameError:
                self.stdout.write(self.style.ERROR('Модель не найдена'))
                return

            # Заполняем модель данными из CSV-файла
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    model.objects.create(**row)

            self.stdout.write(self.style.SUCCESS(
                f'Данные из {csv_file} успешно загружены в базу данных'
            ))

        self.stdout.write(self.style.SUCCESS(
            'Все данные успешно загружены в базу данных!'
        ))