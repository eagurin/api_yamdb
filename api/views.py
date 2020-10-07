import uuid

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import NOREPLY_YAMDB_EMAIL

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title, User
from .permissions import (IsAdminOrReadOnlyPermission, IsAdminUser,
                          IsAuthorOrAdminOrModerator)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer,
                          TokenSerializer, UserSerializer,
                          TitleSerializerRating)
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
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
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
        category = Category.objects.get(
            slug=self.request.data.get("category")
        )
        genres = Genre.objects.filter(
            slug__in=self.request.data.getlist("genre"))

        serializer.save(category=category, genre=genres)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        reviews = title.reviews.all()
        return reviews


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        comments = review.comments.all()
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


class EmailSignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        confirmation_code = uuid.uuid4()
        User.objects.get_or_create(email=email, username=email)
        send_mail(
            'Подтверждение аккаунта',
            f'Ваш ключ активации {confirmation_code}',
            NOREPLY_YAMDB_EMAIL,
            [email],
            fail_silently=True,
        )
        return Response(
            {'result': 'Код подтверждения отправлен на вашу почту'},
            status=200
        )


class CodeConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('confirmation_code')
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=email)
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})
