from django.contrib.auth.models import AbstractUser
from django.db import models

from recipes.constants import FIRST_NAME, LAST_NAME


def avatar_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    return "users/{}.{}".format(instance.username, extension)


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=FIRST_NAME)
    last_name = models.CharField('Фамилия', max_length=LAST_NAME)
    email = models.EmailField('Email', unique=True)
    avatar = models.ImageField('Аватар',
                               upload_to=avatar_directory_path,
                               blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = 'username',

    def __str__(self):
        return f'{self.username}, email: {self.email}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь',
        related_name='authors',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, verbose_name='Автор рецепта',
        related_name='subscribers',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user', 'author')
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='prevent_self_subscription'
            )
        ]
