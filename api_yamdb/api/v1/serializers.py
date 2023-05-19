from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        ValidationError)
from reviews.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class ProfileSerializer(UserSerializer):
    role = CharField(read_only=True)


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    username = CharField(
        max_length=150,
        validators=[
            UnicodeUsernameValidator(),
            RegexValidator(
                regex=r'^(?!me$).*$',
                message='Использовать "me" в качестве username запрещено',
            ),
        ],
    )
    email = EmailField(max_length=254)

    def create(self, validated_data):
        existing_user_by_username = User.objects.filter(
            username=validated_data.get('username')
        ).first()
        existing_user_by_email = User.objects.filter(
            email=validated_data.get('email')
        ).first()
        if any([existing_user_by_username, existing_user_by_email]):
            if existing_user_by_username == existing_user_by_email:
                return existing_user_by_username
            raise ValidationError(
                'Email уже зарегистрирован для другого пользователя.'
            )
        return User.objects.create(**validated_data)


class TokenSerializer(ModelSerializer):
    username = CharField()
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(ModelSerializer):
    class Meta:
        pass


class GenreSerializer(ModelSerializer):
    class Meta:
        pass


class TitleSerializer(ModelSerializer):
    class Meta:
        pass


class TitleCreateUpdateSerializer(ModelSerializer):
    class Meta:
        pass


class ReviewSerializer(ModelSerializer):
    class Meta:
        pass


class CommentSerializer(ModelSerializer):
    class Meta:
        pass
