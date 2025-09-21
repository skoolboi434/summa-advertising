from django.db import models
from adAdmin.models import Account, Publication, Rate, AdminAdType, GLCode
from django.contrib.auth.models import User
from django.utils import timezone

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
    ad_type = models.ForeignKey('adAdmin.AdminAdType', on_delete=models.CASCADE)
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

  

class Classification(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    self_service = models.CharField(max_length=100)
    is_subcategory = models.CharField(max_length=100)
    assigned_gl = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="active")
    created_at = models.DateTimeField(default=timezone.now)

    glCodes = models.ManyToManyField(
        'adAdmin.GLCode',
        related_name="classifications",
        blank=True
    )

    # Self-referential relationship
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,  # null allowed if it has no parent
        null=True,
        blank=True,
        related_name="child_categories"
    )

    class Meta:
        db_table = 'advertising_classification'

    def __str__(self):
        return self.name


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

class ClassifiedImage(models.Model):
    classified_ad = models.ForeignKey(
        'ClassifiedAd', 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='classified_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    # caption = models.CharField(max_length=255, blank=True, null=True)
    # sort_order = models.PositiveIntegerField(default=0)
    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.classified_ad.title} - Image {self.id}"

    class Meta:
        verbose_name = "Classified Image"
        verbose_name_plural = "Classified Images"

class ClassifiedSubcategory(models.Model):
    classification = models.ForeignKey(
        Classification,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'advertising_classifieds_subcategorys'

    def __str__(self):
        return self.name
