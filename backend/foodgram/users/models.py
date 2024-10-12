from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    email = models.EmailField('Email', unique=True)
    avatar = models.ImageField('Аватар', upload_to='users/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    user = models.ForeignKey(
        User, related_name='Пользователь',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='Автор',
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('user')),
                name='prevent_self_subscription'
            )
        ]
