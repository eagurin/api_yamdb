from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from .models import Genre, Title


class TitleFilter(filters.FilterSet):
    class Meta:
        model = Title
        fields = ['genre']

    @property
    def qs(self):
        queryset = super().qs

        genre_slug = self.request.query_params.get('genre', None)
        if genre_slug is not None:
            genre = get_object_or_404(Genre, slug=genre_slug)
            queryset = queryset.filter(genre=genre)

        return queryset
