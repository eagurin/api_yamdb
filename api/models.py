from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Категория")
    slug = models.SlugField(max_length=50, verbose_name="slug", unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=150, verbose_name="Жанр")
    slug = models.SlugField(max_length=50, verbose_name="slug", unique=True)


class Title(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название фильма")
    year = models.IntegerField(
        validators=[MinValueValidator(1950), MaxValueValidator(2030)],
        verbose_name="Год выпуска"
    )
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='genre')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 verbose_name="Категория")


class Reviews(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
        related_name="review_title")
    text = models.TextField(verbose_name="Отзыв")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="review_author")
    score = models.IntegerField(
        validators =[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка"
    )
    pub_date = models.DateTimeField(verbose_name="date published", 
        auto_now_add=True)


class Comments(models.Model):
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE,
        related_name="comment_review")
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="comment_author") 
    pub_date = models.DateTimeField(verbose_name="date published", 
        auto_now_add=True)     


    



