from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import People, Options

@receiver(post_save, sender=People)
def create_options_for_new_user(sender, instance, created, **kwargs):
    if created:
        Options.objects.get_or_create(People_ID=instance)