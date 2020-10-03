from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import APIException,ParseError
from rest_framework.views import exception_handler
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .filters import TitleFilter
from .models import Category, Comments, Genre, Reviews, Title, User
from .permissions import (IsAdminOrReadOnlyPermission, IsAdminUser,
                          IsAuthorOrAdminOrModerator, IsOwnerOrReadOnly)
from .serializers import *
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
    queryset = Title.objects.all().annotate(rating=Avg('review_title__score'))
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleSerializerRating
        return TitleSerializer

    def perform_update(self, serializer):
        category = get_object_or_404(
            Category,
            slug=self.request.data.get("category"))

        serializer.save(category=category)

    def perform_create(self, serializer):
        category = Category.objects.get(slug=self.request.data.get("category"))
        genres = Genre.objects.filter(
            slug__in=self.request.data.getlist("genre"))

        serializer.save(category=category, genre=genres)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):  
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        try:
            serializer.save(author=self.request.user, title=title) 
        except IntegrityError:
            raise ParseError(detail="Ошибка уникальности")

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        reviews = title.review_title.all()
        return reviews


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):  
        review = get_object_or_404(Reviews, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review) 

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
    search_fields = ["=name", ]
    lookup_field = "username"

    @action(detail=False,
            permission_classes=[permissions.IsAuthenticated],
            methods=['PATCH', 'GET']
            )
    def me(self, request, *args, **kwargs):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
