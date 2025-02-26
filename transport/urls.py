from django.urls import path

from .views import load_md_to_db, process_image_with_ollama

urlpatterns = [
  path('load-md/', load_md_to_db, name='load_md_to_db'),
  path('create-md/', process_image_with_ollama,
       name='process_image_with_ollama')
]
