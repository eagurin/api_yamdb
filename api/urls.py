from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import *

router = DefaultRouter()
router.register('users', UserViewSet)

router.register('titles', TitleViewSet)

router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)

router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewsViewSet)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentsViewSet
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'
         ),
    path('v1/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'
         ),
    #path('v1/auth/token/', CodeConfirmView.as_view()),
    #path('v1/auth/email/', EmailSignUpView.as_view()),
]
