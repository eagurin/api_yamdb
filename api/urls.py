from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from api import views
from api.views import (GenreViewSet, CategoryViewSet, 
                TitleViewSet, ReviewsViewSet, CommentsViewSet, UserViewSet)

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='Title')
router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewsViewSet)
router.register(r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments', CommentsViewSet)
router.register(r'users', UserViewSet, basename='User')

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('v1/genres/',
         views.GenreViewSet.as_view({'get': 'list', 'post': 'create'}),
         name="genres"),
    path('v1/genres/<str:slug>/',
         views.GenreViewSet.as_view({'delete': 'destroy'}),
         name="genres_remove"),
    path('v1/categories/', views.CategoryViewSet.as_view(
        {'get': 'list', 'post': 'create'}),
         name="categories"),
    path('v1/categories/<str:slug>/',
         views.CategoryViewSet.as_view({'delete': 'destroy'}),
         name="categories_remove"),
]
