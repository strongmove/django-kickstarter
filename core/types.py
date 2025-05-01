from django.contrib.auth import get_user_model
import strawberry.django
from strawberry import auto
from . import models

User = get_user_model()


@strawberry.django.type(User)
class UserModelType:
    email: auto
    id: auto
    username: auto
