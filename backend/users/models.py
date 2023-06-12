from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'Эл. почта',
        max_length=settings.EMAIL_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.USER_FIELD_LENGTH,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.USER_FIELD_LENGTH,
        blank=False,
    )
    password = models.CharField(
        'Пароль',
        max_length=settings.USER_FIELD_LENGTH,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='self_subscribe'
            ),
        ]

    def __str__(self):
        return f'{self.user}-{self.author}'
