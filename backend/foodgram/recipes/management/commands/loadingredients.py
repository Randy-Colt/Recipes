from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


FILE_DIR = settings.BASE_DIR / 'data/ingredients.csv'


class Command(BaseCommand):
    help = 'Загружает ингридиенты из файла CSV в базу данных'

    def handle(self, *args, **options):
        with open(FILE_DIR, encoding='utf-8') as file:
            reader = DictReader(file, ('name', 'measurement_unit'))
            self.stdout.write('Начат импорт данных')
            Ingredient.objects.bulk_create(
                (Ingredient(**item) for item in reader)
            )
            self.stdout.write('Импорт закончен без ошибок')
