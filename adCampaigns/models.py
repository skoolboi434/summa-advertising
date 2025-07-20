from django.db import models

# models.py (in your adCampaigns app)

from django.db import models

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

class SalesPerson(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=100, default=None,null=True,blank=True)
    city = models.CharField(max_length=100, default=None,null=True,blank=True)
    state = models.CharField(max_length=100, default=None,null=True,blank=True)
    zip_code = models.CharField(max_length=100, default=None,null=True,blank=True)
    email = models.CharField(max_length=100, default=None,null=True,blank=True)
    phone_number = models.CharField(max_length=100, null=True, default=None)
    active = models.BooleanField(default=True)
    commission_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'advertising_salesperson'

