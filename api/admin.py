from django.contrib import admin

from .models import Category, Genre, Title


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "category")
    empty_value_display = "-пусто-"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    empty_value_display = "-пусто-"


admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
