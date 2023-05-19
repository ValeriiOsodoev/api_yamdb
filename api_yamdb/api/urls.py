from django.urls import include, path


urlpatterns = [path('v1/', include('api.v1.urls'))]
from .views import APIGetToken, APISignup, UsersViewSet, CommentViewSet, ReviewViewSet

app_name = 'api'

router = SimpleRouter()
router.register('users', UsersViewSet, basename='users')
router.register("reviews", ReviewViewSet)
router.register(r"reviews/(?P<review_id>\d+)/comments",
                CommentViewSet, basename='comments')
router.register(r"groups", CategoryViewSet)

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
