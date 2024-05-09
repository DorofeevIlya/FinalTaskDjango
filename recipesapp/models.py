from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000)
    cook_steps = models.TextField()
    cook_time = models.IntegerField()
    ingredients = models.TextField()
    image = models.ImageField(upload_to='images/')
    ingredients = models.TextField()
    complexity = models.CharField(max_length=15, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='other')

    @property
    def created_at_f(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M')

    def __str__(self):
        return f'{self.name}/{self.category} (добавил {self.author} {self.created_at_f})'