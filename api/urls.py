from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views
from api.views import GenreViewSet, CategoryViewSet, TitleViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='Title')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/genres/',
         views.GenreViewSet.as_view(
             {'get': 'list', 'post': 'create', 'delete': 'destroy'}),
         name="genres"),
    path('v1/categories/',
         views.CategoryViewSet.as_view(
             {'get': 'list', 'post': 'create', 'delete': 'destroy'}),
         name="categories"),
]
