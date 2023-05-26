from api.v1.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                          ReviewViewSet, SignUPView, TitleViewSet, TokenView,
                          UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'auth/',
        include(
            [
                path('signup/', SignUPView.as_view()),
                path('token/', TokenView.as_view()),
            ]
        ),
    ),
    path('', include(router.urls)),
]
