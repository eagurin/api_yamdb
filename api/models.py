from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    
    class UserRole:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        choices = [
            (USER, 'user'),
            (ADMIN, 'admin'),
            (MODERATOR, 'moderator'),
        ]

    email = models.EmailField(blank=False, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=25, choices=UserRole.choices, default=UserRole.USER)
    confirmation_code = models.CharField(max_length=100, blank=True, )

    def __str__(self):
        return self.username
        

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
