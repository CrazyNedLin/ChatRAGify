from django.urls import path

from .views import chat_with_memory

urlpatterns = [
  path("chat/", chat_with_memory, name="chat_with_memory"),
]
