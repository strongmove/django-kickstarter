import strawberry
import strawberry.django
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_django.pagination import OffsetPaginated

from .types import UserModelType


@strawberry.type
class Query:
    user: UserModelType = strawberry.django.field()
    users: OffsetPaginated[UserModelType] = strawberry.django.offset_paginated()


schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
