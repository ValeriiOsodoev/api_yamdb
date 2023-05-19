from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUPView, TokenView, UserViewSet

router = DefaultRouter()

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
