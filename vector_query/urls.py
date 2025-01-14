from django.urls import path

from .views import vector_search

urlpatterns = [
  path("search/", vector_search, name="vector_search"),
]
