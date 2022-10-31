from django.contrib.auth.models import AbstractUser
from accounts.managers import UserManager
from django.db import models
from django.db.models import TextChoices

class GenderChoices(TextChoices):
    MAN = 'Мужской','Мужской'
    WOMAN = 'Женский','Женский'

class Account(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        unique=True,
        blank=True,
        max_length=50)
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        blank=True)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='profile',
        verbose_name='Аватар'
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=50)
    additional = models.TextField(
        verbose_name="Информация о пользователе",
        max_length=1000)
    phone = models.CharField(
        verbose_name="Номер телефона",
        max_length=12)
    gender = models.CharField(
        choices=GenderChoices.choices,
        verbose_name='Пол',
        null=True,
        blank=True,
        max_length=50)
    liked_posts = models.ManyToManyField(
        verbose_name='Понравившиеся публикации',
        to='posts.Post',
        related_name='user_likes')
    subscriptions = models.ManyToManyField(
        verbose_name='Подписки',
        to='accounts.Account',
        related_name='subscribers')
    commented_posts = models.ManyToManyField(
        verbose_name='Прокомментированные публикации',
        to='posts.Post',
        related_name='user_comments')
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Время изменения',
        auto_now=True)
    is_deleted = models.BooleanField(
        verbose_name='Удалено',
        default=False,
        null=False
    )

    def __str__(self):
        return f"{self.email}-{self.username}-{self.first_name}"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
