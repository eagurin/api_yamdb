from rest_framework import filters, mixins, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
##from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets, permissions
from rest_framework.response import Response

from .serializers import *
from .models import Genre, Category, Title, Reviews, Comments, User
from .permissions import (IsAdminUser, IsAdminOrReadOnlyPermission, IsAuthorOrAdminOrModerator)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .utils import CreateListViewSet


class GenreViewSet(CreateListViewSet):
    permission_classes = [IsAdminOrReadOnlyPermission, ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class CategoryViewSet(CreateListViewSet):
    permission_classes = [IsAdminOrReadOnlyPermission, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyPermission, ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        reviews = title.review_title.all()
        return reviews


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrAdminOrModerator, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        comments = review.comment_review.all()
        return comments


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", ]
    lookup_field = "username"
