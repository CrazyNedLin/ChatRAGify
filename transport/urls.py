from django.urls import path

from .views import load_md_to_db

urlpatterns = [
  path('load-md/', load_md_to_db, name='load_md_to_db'),
]
