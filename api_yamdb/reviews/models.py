from django.contrib.auth.models import AbstractUser
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
>>>>>>> upd
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
<<<<<<< HEAD
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
>>>>>>> upd
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
=======
        max_length=30, choices=USER_ROLES, default=USER, verbose_name='Роль'
>>>>>>> upd
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения', max_length=36, blank=True, null=True
    )
<<<<<<< HEAD
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
    name = models.CharField(max_length=256, blank=False)
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
        blank=False,
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
=======

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
    
    def __str__(self):
        return self.username


<<<<<<< HEAD
    def __str__(self):
        return self.username
>>>>>>> upd
=======
class Genre(models.Model):
    pass


class Category(models.Model):
    pass


class Title(models.Model):
    pass


class GenreTitle(models.Model):
    pass


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
<<<<<<< HEAD
    pass
>>>>>>> upd
=======
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
>>>>>>> Правки
