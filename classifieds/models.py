from django.db import models
from adAdmin.models import Account, Publication
from django.contrib.auth.models import User

#from adAdmin.models import AdminAdType

class ClassifiedAd(models.Model):
    name = models.CharField(max_length=255)
    account = models.ForeignKey(
        'adAdmin.Account',  # app_label.ModelName
        on_delete=models.CASCADE,
        related_name='classified_ads'
    )
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    classification = models.ForeignKey('Classification', on_delete=models.CASCADE, null=True, blank=True)
    #classification = models.ForeignKey('Classification', on_delete=models.CASCADE)
    #content = RichTextField(null=True, blank=True)
    content = models.TextField()
    recurring = models.BooleanField(default=False)
    recurring_amount = models.CharField(max_length=50)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    submitter = models.CharField(max_length=255, default=None)
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='on hold') # this will change once the ad is paid for 
    line_count = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
    size = models.CharField(max_length=25, blank=True, null=True)  # Updated
    columns = models.IntegerField(default=0)
    column_length = models.IntegerField(default=0)
    unit = models.CharField(max_length=25, blank=True,null=True)
    words =models.CharField(max_length=25, blank=True,null=True)
    page_number = models.CharField(max_length=25, blank=True,null=True)
    overide_total=models.CharField(max_length=25, blank=True,null=True)
    custom_total = models.CharField(max_length=25, blank=True,null=True)
    layout_notes=models.TextField(blank=True,null=True)
    desgin_notes=models.TextField(blank=True,null=True)
    account_notes=models.TextField(blank=True,null=True)
    rate = models.CharField(max_length=250, blank=True, null=True)  # Updated

    # conversion_unit = models.CharField(max_length=20)
    ad_type = models.ForeignKey('AdminAdType', on_delete=models.CASCADE)
    # TODO - add a field for picture of the classified ad 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'advertising_classifiedad'


class ClassifiedCampaignSummary(models.Model):
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
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
        db_table = "advertising_campaign_summary"

class AdminAdType(models.Model):
    code = models.CharField(max_length=100, default=None)
    name = models.CharField(max_length=255, default=None)
    #default_rate = models.ForeignKey('Rate', on_delete=models.CASCADE, default=None)
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'advertising_adminadtype'

    def __str__(self):
        return self.code  

class Classification(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'advertising_classification'

    def __str__(self):
        return self.name

from django.db import models

class ProductAddon(models.Model):
    ADDON_TYPE_CHOICES = [
        ('word_count', 'Word Count Increase'),
        ('additional_publication', 'Additional Publication'),
        # Add more types here as needed
    ]

    addon_type = models.CharField(max_length=100, choices=ADDON_TYPE_CHOICES)
    label = models.CharField(max_length=255)  # e.g., "Increase by 35 Words" or "Anson Record"
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "advertising_classifieds_addons"
        verbose_name = "Product Addon"
        verbose_name_plural = "Product Addons"
        ordering = ['addon_type', 'label']

    def __str__(self):
        return f"{self.label} (${self.price})"
