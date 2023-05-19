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


class Review(models.Model):
    text = models.TextField(
        help_text='Введите текст поста',
        verbose_name="Текст"
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='reviews/',
        null=True,
        blank=True,
        verbose_name='Картинка'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='review',
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Выберите категорию'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        help_text='Введите комментарий',
        verbose_name='Текст комментария',
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
