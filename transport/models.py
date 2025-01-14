from django.db import models
from pgvector.django import VectorField


class TransportationData(models.Model):
  district = models.CharField(max_length=100)
  green_transport = models.FloatField()
  public_transport = models.FloatField()
  non_motorized = models.FloatField()
  walking = models.FloatField()
  bike = models.FloatField()
  private_motorized = models.FloatField()
  most_used_public_transport = models.FloatField()
  embedding = VectorField(dimensions=3072)  # Llama3.2 向量大小

  def __str__(self):
    return self.district
