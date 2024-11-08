import os
from random import choices

from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save, pre_save
from django.db.utils import IntegrityError
from django.dispatch import receiver

from recipes.constants import CHARACTERS, LENGHT
from recipes.models import Recipe, ShortLinkConverter


User = get_user_model()


@receiver(post_save, sender=Recipe)
def create_converter(sender, instance, created, **kwargs):
    if created:
        while True:
            try:
                short_link = ''.join(choices(CHARACTERS, k=LENGHT))
                ShortLinkConverter.objects.create(
                    recipe=instance, short_link=short_link)
                break
            except IntegrityError:
                continue


@receiver(pre_save, sender=User)
@receiver(pre_save, sender=Recipe)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Автоудаление старого изображения из файловой системы.

    Срабатывает, если изображение рецепта или аватар пользователя изменены.
    """
    if not instance.pk:
        return False
    new_file = instance.avatar if sender.__name__ == 'User' else instance.image
    if not new_file:
        return False
    try:
        if sender.__name__ == 'User':
            old_file = sender.objects.get(pk=instance.pk).avatar
        else:
            old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False
    if old_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_delete, sender=User)
@receiver(post_delete, sender=Recipe)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Автоудаление изображения из файловой системы.

    Срабатывает, если удалён рецепт или пользователь.
    """
    file = instance.avatar if sender.__name__ == 'User' else instance.image
    if file:
        if os.path.isfile(file.path):
            os.remove(file.path)
