from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    APISignup,
    CategoriesViewSet,
    GenreViewSet,
    TitleViewSet,
    UsersViewSet,
)

app_name = 'api'

router = SimpleRouter()
router.register(
    'users',
    UsersViewSet,
    basename='users'
)
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
