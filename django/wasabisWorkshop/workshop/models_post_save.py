from .models import Score

from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=Score)
# def save_profile(sender, instance, **kwargs):
#     if instance.answered:
#         instance.delete()
