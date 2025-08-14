from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone

class AdvertisingCampaignSummary(models.Model):
    id = models.IntegerField(primary_key=True)
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    brief = models.CharField(max_length=255)
    advertiser_id = models.IntegerField(null=True)
    advertiser_name = models.CharField(max_length=50, null=True)
    contact_id = models.IntegerField(null=True)
    sales_contact = models.CharField(max_length=50, null=True)
    total_sub = models.IntegerField()
    total_adjustment = models.IntegerField()
    total_campaign = models.IntegerField()
    campaign_detail = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'advertising_campaign_summary'  # matches existing DB table
        managed = False  # disables migrations for this table

