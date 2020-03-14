from django.db import models

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=512)
    expiry_date = models.DateField(blank=True)
    image = models.ImageField(blank=True)

    class Meta:
        verbose_name_plural = 'food'
