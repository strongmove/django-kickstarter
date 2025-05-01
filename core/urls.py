from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView
from .views import IndexView
from .schema import schema


urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("graphql", csrf_exempt(AsyncGraphQLView.as_view(schema=schema))),
]
