from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUPView, TokenView, UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

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
