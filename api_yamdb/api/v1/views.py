from api.mixins import ListCreateDestroyViewSet
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User, Category, Genre, Title
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db.models import F

from .permissions import AdminRules, UserAccess, AccessOrReadOnly, ReadOnly, IsAdminOrReadOnly
from .serializers import (ProfileSerializer, SignUpSerializer, TokenSerializer,
                          UserSerializer, CategorySerializer, GenreSerializer, TitleSerializer)

HTTP_METHOD = ('get', 'post', 'patch', 'delete')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminRules,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    http_method_names = HTTP_METHOD
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        serializer_class=ProfileSerializer,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            try:
                serializer.is_valid(raise_exception=True)
            except ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SignUPView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = (
            confirmation_code  # Присвоение значения confirmation_code
        )
        user.save()  # Сохранение пользователя с заполненным confirmation_code
        send_mail(
            subject='Confirmation code',
            message=f'{confirmation_code}',
            from_email=settings.FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == confirmation_code:
            jwt_token = AccessToken.for_user(user)
            return Response(
                {'token': f'{jwt_token}'}, status=status.HTTP_200_OK
            )
        return Response(
            {
                'message': 'Это 400 ошибка, потому что '
                'отсутствует обязательное поле для создания токена '
                'или оно некорректно'
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet модели Categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    pagination_class = PageNumberPagination
    
    def retrieve(self, request, *args, **kwargs):
        """Переопределение метода retrieve для запрета GET-запросов."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """Переопределение метода destroy для удаления категории."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, *args, **kwargs):
        """Переопределение метода partial_update для запрета PATCH-запросов."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly, ]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'slug']
    filterset_fields = ['name', 'slug']

    def retrieve(self, request, *args, **kwargs):
        """Переопределение метода retrieve для запрета GET-запросов."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """Переопределение метода destroy для удаления категории."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, *args, **kwargs):
        """Переопределение метода partial_update для запрета PATCH-запросов."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        category_name=F('category__name'),
        category_slug=F('category__slug'),
    )
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
