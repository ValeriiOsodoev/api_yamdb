from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    groups = models.ManyToManyField(
        to='auth.Group',
        related_name='customuser_groups',  # добавляем related_name здесь
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all '
        'permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        to='auth.Permission',
        related_name='customuser_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
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
    @property
    def is_user(self):
        return self.role == USER
    @property
    def is_admin(self):
        return self.role == ADMIN
    @property
    def is_moderator(self):
        return self.role == MODERATOR
    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    def __str__(self):
        return self.username



class Categories(models.Model):
    """Модель категории."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """"Модель произведений."""
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles',
        blank=True, 
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
    )
    name = models.CharField(
        max_length=300,
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
        return self.category, self.genre, self.name, self.description, self.year
