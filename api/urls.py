from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, ReviewsViewSet, CommentsViewSet,
                    TitleViewSet, GenreViewSet, CategoryViewSet, 
                    EmailSignUpView, CodeConfirmView
                   )

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewsViewSet)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentsViewSet
)
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', EmailSignUpView.as_view()),
    path('v1/auth/token/', CodeConfirmView.as_view()),
]
