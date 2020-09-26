from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Категория")
    slug = models.SlugField(max_length=50, verbose_name="slug", unique=True)


class Title(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название фильма")
    year = models.IntegerField(
        validators=[MinValueValidator(1950), MaxValueValidator(2030)],
        verbose_name="Год выпуска"
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 related_name='categories',
                                 verbose_name="Категория")


class Genre(models.Model):
    name = models.CharField(max_length=150, verbose_name="Жанр")
    slug = models.SlugField(max_length=50, verbose_name="slug", unique=True)




