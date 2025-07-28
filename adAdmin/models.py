from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'advertising_role'

class Region(models.Model):
    name = models.TextField()
    code = models.TextField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    class Meta:
        db_table = 'advertising_region'


