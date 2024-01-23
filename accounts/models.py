import uuid

from allauth.account.signals import user_signed_up
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.dispatch import receiver


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


@receiver(user_signed_up)
def after_user_signed_up(sender, request, user, *args, **kwargs):
    try:
        default_user_group = Group.objects.get(name=settings.DEFAULT_USER_GROUP_NAME)
    except Group.DoesNotExist:
        default_user_group = Group(name=settings.DEFAULT_USER_GROUP_NAME)
        default_user_group.save()
    user.groups.add(default_user_group)
