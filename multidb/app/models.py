from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50, help_text='name')
    age = models.IntegerField()

    class Meta:
        db_table = 'person'