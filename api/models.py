from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    )
    email = models.EmailField(
        help_text='email address', blank=False, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=25, choices=USER_ROLES, default="user")
    confirmation_code = models.CharField(
        max_length=100, unique=True, blank=True, null=True)
    username = models.CharField(
        max_length=30, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


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
    #rating = models.IntegerField(blank=True, null=True)
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
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка"
    )
    pub_date = models.DateTimeField(verbose_name="date published",
                                    auto_now_add=True)
    
    class Meta:
        unique_together=['author', 'title']
        ordering = ['-id']


class Comments(models.Model):
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE,
                               related_name="comment_review")
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comment_author")
    pub_date = models.DateTimeField(verbose_name="date published",
                                    auto_now_add=True)

    class Meta:
        ordering = ['-id']