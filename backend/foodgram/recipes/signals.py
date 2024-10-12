from string import ascii_letters, digits
from random import choices

from django.db.utils import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from recipes.constants import LENGHT
from recipes.models import ShortLinkConverter, Recipe


@receiver(post_save, sender=Recipe)
def create_converter(sender, instance, created, **kwargs):
    if created:
        characters = ascii_letters + digits
        while True:
            try:
                short_link = ''.join(choices(characters, k=LENGHT))
                ShortLinkConverter.objects.create(
                    recipe=instance, short_link=short_link)
                break
            except IntegrityError:
                continue
