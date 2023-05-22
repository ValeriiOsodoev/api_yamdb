from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[
            UnicodeUsernameValidator(),
            RegexValidator(
                regex=r'^(?!me$).*$',
                message='Использовать "me" в качестве username запрещено',
            ),
        ],
    )
    email = models.EmailField(
        unique=True, verbose_name='Адрес электронной почты'
    )
    role = models.CharField(
        max_length=30, choices=USER_ROLES, default=USER, verbose_name='Роль'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения', max_length=36, blank=True, null=True
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )


class Title(models.Model):
    """"Модель произведений."""
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles',
        blank=True, 
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения.'
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Представление произведения.'
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='Год произведения.',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    pass
