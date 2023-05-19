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

from .permissions import AdminRules
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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('name', 'slug')
    filterset_fields = ('name', 'slug')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = TitleSerializer
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
