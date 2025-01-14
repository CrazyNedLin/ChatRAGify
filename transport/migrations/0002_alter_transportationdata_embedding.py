# Generated by Django 5.1.4 on 2025-01-10 04:36

import pgvector.django.vector
from django.db import migrations


class Migration(migrations.Migration):
  dependencies = [
    ("transport", "0001_initial"),
  ]

  operations = [
    migrations.AlterField(
        model_name="transportationdata",
        name="embedding",
        field=pgvector.django.vector.VectorField(dimensions=3072),
    ),
  ]
