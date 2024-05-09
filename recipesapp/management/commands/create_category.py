from django.core.management.base import BaseCommand
from recipesapp.models import Category


class Command(BaseCommand):
    help = "Create category."

    def handle(self, *args, **kwargs):
        category = Category(name='Гарниры', description='Украшение основного (мясного или рыбного) блюда.')
        category.save()
        self.stdout.write(f'{category}')
