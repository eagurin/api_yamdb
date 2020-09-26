from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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
                                 related_name="categories",
                                 verbose_name="Категория")


class Genre(models.Model):
    name = models.CharField(max_length=150, verbose_name="Жанр")
    slug = models.SlugField(max_length=50, verbose_name="slug", unique=True)


class Reviews(models.model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
        related_name="review_title")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="review_author")
    text = models.TextField(verbose_name="Отзыв")
    score = models.IntegerField(
        validators =[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка"
    )
    pub_date = models.DateTimeField(verbose_name="date published", 
        auto_now_add=True)


class Comments(models.model):
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE,
        related_name="comment_review")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="comment_author") 
    text = models.TextField(verbose_name="Комментарий")
    pub_date = models.DateTimeField(verbose_name="date published", 
        auto_now_add=True)    


    



