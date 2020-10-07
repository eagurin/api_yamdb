from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "category")
    empty_value_display = "-пусто-"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", "author", "score", "pub_date")
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "text", "author", "pub_date")
    empty_value_display = "-пусто-"


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "username", "email", "bio", "role")
    empty_value_display = "-пусто-"

admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)