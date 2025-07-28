from django.db import models
from django.utils import timezone
from adAdmin.models import Status
from adAdmin.models import Region, Role 

class AdvertisingUser(models.Model):
    id = models.AutoField(primary_key=True)
    
    # Core profile fields
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    username    = models.CharField(max_length=100, unique=True)
    nickname    = models.CharField(max_length=100, blank=True, null=True)
    email       = models.EmailField(max_length=150, unique=True)
    phone       = models.CharField(max_length=50, blank=True, null=True)
    website     = models.URLField(blank=True, null=True)
    bio         = models.TextField(blank=True, null=True)
    language    = models.CharField(max_length=10, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    commission = models.FloatField(default=0.0)

    # FK to your statuses table
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='status_id'
    )

    # DB is already setting these (or you can set them manually)
    created_at  = models.DateTimeField(blank=True, null=True)
    updated_at  = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'advertising_users'
        managed  = False   # <-- important: don't let Django try to migrate it

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()