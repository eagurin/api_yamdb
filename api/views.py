import uuid

from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import NOREPLY_YAMDB_EMAIL

from .filters import TitleFilter
from .models import Category, Comments, Genre, Reviews, Title, User
from .permissions import (IsAdminOrReadOnlyPermission, IsAdminUser,
                          IsAuthorOrAdminOrModerator)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer, SignUpSerializer,
                          TitleSerializer, TitleSerializerRating,
                          TokenSerializer, UserSerializer)
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
        category = Category.objects.get(
            slug=self.request.data.get("category")
        )
        genres = Genre.objects.filter(
            slug__in=self.request.data.getlist("genre"))

        serializer.save(category=category, genre=genres)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator]
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
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator]
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


class EmailSignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            confirmation_code = uuid.uuid4()
            User.objects.create(
                email=email, username=str(email),
                confirmation_code=confirmation_code,
                is_active=False
            )
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                email=serializer.data['email'],
                confirmation_code=serializer.data['confirmation_code']
            )
        except User.DoesNotExist:
            return Response(
                data={'detail': 'Invalid email or code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user.is_active = True
            user.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh_token.access_token)
            })
