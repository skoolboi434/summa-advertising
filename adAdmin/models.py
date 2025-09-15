from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User


class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"
        db_table = "company_info"

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'advertising_role'


class AdminAdType(models.Model):
    code = models.CharField(max_length=100, default=None)
    name = models.CharField(max_length=255, default=None)
    default_rate = models.ForeignKey('Rate', on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=100, default="active")
    created_at = models.DateTimeField(default=timezone.now)

    publications = models.ManyToManyField(
        'Publication', 
        related_name="adTypes", 
        blank=True
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_adTypes")
    
    class Meta:
        db_table = 'advertising_adminadtype'

    def __str__(self):
        return self.code


class Region(models.Model):
    name = models.TextField()
    code = models.TextField()
    status = models.CharField(max_length=100, default="active")
    

    # Many-to-many relationship to Publication
    publications = models.ManyToManyField(
        'Publication', 
        related_name="regions", 
        blank=True
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_regions")

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'advertising_region'

    def __str__(self):
        return self.name

class AdCriteria(models.Model):
    name = models.TextField()
    code = models.TextField()
    status = models.CharField(max_length=100, default="active")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_ad_criterias")
    

    # Many-to-many relationship to Publication
    publications = models.ManyToManyField(
        'Publication', 
        related_name="ad_criterias", 
        blank=True
    )

    class Meta:
        db_table = 'advertising_ad_criteria'

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.TextField()
    code = models.TextField()
    status = models.CharField(max_length=100, default="active")
    sub_section = models.CharField(max_length=255, default="None")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_sections")
    

    # Many-to-many relationship to Publication
    publications = models.ManyToManyField(
        'Publication', 
        related_name="sections", 
        blank=True
    )

    class Meta:
        db_table = 'advertising_sections'

    def __str__(self):
        return self.name



class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'advertising_status'  # matches your manual table name

    def __str__(self):
        return self.name

class Publication(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    spot_color = models.CharField(max_length=50)
    charge_tax = models.BooleanField(default=False)
    credit_memo = models.TextField(default=None)

    # Many-to-many field to classifications
    classifications = models.ManyToManyField(
        'classifieds.Classification',   # app_label.ModelName
        related_name="publications",
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'advertising_publication'

class Account(models.Model):
    # Old fields
    submitter = models.CharField(max_length=100, null=True, blank=True)
    account_type = models.ForeignKey('AccountType', null=True, on_delete=SET_NULL)
    sales_person = models.ForeignKey('SalesPerson', null=True, on_delete=SET_NULL, default=None)
    industry_code = models.ForeignKey('IndustryCode', null=True, on_delete=SET_NULL, default=None, related_name='account_industry_code')
    name = models.CharField(max_length=100, null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_name_first = models.CharField(max_length=100, null=True, blank=True)
    contact_name_last = models.CharField(max_length=100, null=True, blank=True)
    company_name_1 = models.CharField(max_length=255, null=True, blank=True)
    company_name_2 = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    legacy_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=19, decimal_places=2, null=True, blank=True)
    total_spent = models.FloatField(default=0.00, null=True, blank=True)
    last_activity = models.CharField(max_length=100, null=True, blank=True)
    last_ad_run = models.DateField(default=None, null=True, blank=True)
    can_run_ads = models.BooleanField(default=True, null=True, blank=True)
    default_publication = models.ForeignKey('Publication', on_delete=SET_NULL, null=True, default=None)
    can_accept_checks = models.BooleanField(default=True, null=True, blank=True)
    tax_exempt = models.BooleanField(default=False, null=True, blank=True)
    last_payment_date = models.CharField(max_length=100, null=True, blank=True)
    invoice_frequency = models.CharField(default='period', max_length=45, null=True, blank=True)
    invoice_type = models.CharField(default='email', max_length=45, null=True, blank=True)
    mail_invoice_charge = models.FloatField(default=0.00, null=True, blank=True)
    credit = models.DecimalField(default=0, max_digits=19, decimal_places=2, null=True, blank=True)
    credit_limit = models.DecimalField(default=1000.0, max_digits=19, decimal_places=2, null=True, blank=True)
    write_off_amount = models.IntegerField(default=0, null=True, blank=True)
    write_off_period = models.CharField(max_length=30, default=None, null=True, blank=True)
    prepay_required = models.BooleanField(default=False, null=True, blank=True)
    billing_email = models.EmailField(max_length=100, null=True, blank=True)
    billing_address = models.EmailField(max_length=100, null=True, blank=True)
    billing_city = models.EmailField(max_length=100, null=True, blank=True)
    billing_state = models.EmailField(max_length=100, null=True, blank=True)
    billing_zip_code = models.EmailField(max_length=100, null=True, blank=True)
    status = models.IntegerField(default=0, null=True, blank=True)
    market_code = models.ForeignKey('MarketCode', on_delete=SET_NULL, null=True, blank=True,related_name='accounts')   
     # New fields from the Excel sheet
    sort_2 = models.CharField(max_length=100, null=True, blank=True)
    customer_number = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    alt_account_number = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    account_type_code = models.CharField(max_length=100, null=True, blank=True)
    account_type_descr = models.CharField(max_length=255, null=True, blank=True)
    business_unit = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    export_ar = models.BooleanField(default=False)
    subscriber = models.BooleanField(default=False)
    in_collection = models.BooleanField(default=False)
    notify_manager = models.BooleanField(default=False)
    do_not_publish = models.BooleanField(default=False)
    no_new_ads = models.BooleanField(default=False)
    setaside_new_ads_code = models.CharField(max_length=100, null=True, blank=True)
    setaside_new_ads_descr = models.CharField(max_length=255, null=True, blank=True)
    prepay_cash_required = models.BooleanField(default=False)
    po_required = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    stop_date = models.DateField(null=True, blank=True)
    run_date = models.DateField(null=True, blank=True)
    label_line_1 = models.CharField(max_length=255, null=True, blank=True)
    label_line_2 = models.CharField(max_length=255, null=True, blank=True)
    label_line_3 = models.CharField(max_length=255, null=True, blank=True)
    label_line_4 = models.CharField(max_length=255, null=True, blank=True)
    label_line_5 = models.CharField(max_length=255, null=True, blank=True)
    label_line_6 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_account_notes', 'Can view account notes'),
            ('can_view_sales_rep_notes', 'Can view sales rep notes'),
            ('can_add_sales_rep_notes', 'Can add sales rep notes'),
            # TODO - add permission to restrict access to changing sales rep field
        )
        db_table = 'advertising_account'

class Rate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pricing = models.BooleanField(default=False)
    measurement_type = models.CharField(max_length=100)
    extra_groups = models.CharField(max_length=100)
    tax_category = models.CharField(max_length=100, default="No Tax")
    override_privileges= models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    assigned_groups = models.BooleanField(default=True)
    ad_type_id = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    insertion_min = models.CharField(max_length=255)
    insertion_max = models.CharField(max_length=255)
    line_for_ad_min = models.CharField(max_length=255)
    line_for_ad_max = models.CharField(max_length=255)
    insertion_count = models.IntegerField()
    base_cost = models.CharField(max_length=100)
    base_count = models.CharField(max_length=100)
    additional_cost = models.CharField(max_length=100)
    additional_count = models.CharField(max_length=100)
    charge_for = models.BooleanField()
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    default_gl_code = models.ForeignKey('GLCode', on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    product = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("can_deactivate_rate", "Can deactivate rate"),
            ("can_reactivate_rate", "Can reactivate rate"),
            ("can_view_hidden_rates", "Can view hidden rates"),
            ("can_lock_rates", "Can lock rates"),
            ('can_create_rates', "Can create rates")
        )

        db_table = 'advertising_rate'

class GLCode(models.Model):
    code = models.CharField(max_length=4, unique=True)
    description = models.CharField(max_length=100)
    # company = models.ForeignKey('Company', on_delete=models.CASCADE)
    pl_type = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        permissions = (
            ('can_create_gl_codes', 'Can create GL Codes'),
            ('can_edit_gl_codes', 'Can edit GL Codes'),
            ('can_import_gl_codes', 'Can import GL Codes'),
            ('can_export_gl_codes', 'Can export GL Codes'),
        )

    class Meta:
        db_table = 'advertising_glcode'

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

class AccountType(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status = models.ForeignKey('adAdmin.Status', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'advertising_accounttype'

class IndustryCode(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    account = models.ForeignKey('Account', on_delete=CASCADE,null=True,blank=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'advertising_industrycode'

class MarketCode(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    #description = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="active")
    #account = models.ForeignKey('Account', on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_market_code")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "advertising_marketcode"



class CompanyContact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    account = models.ForeignKey('Account', on_delete=CASCADE)
    department = models.ForeignKey('CompanyDepartment', on_delete=CASCADE)
    default = models.IntegerField()
    active = models.IntegerField()
    class Meta:
        db_table = 'advertising_companycontact'

class CompanyDepartment(models.Model):
    name = models.CharField(max_length=30, unique=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'advertising_department'

class AccountNote(models.Model):
    note = models.TextField()
    timestamp = models.DateTimeField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    updatedAt = models.DateTimeField()

    def __str__(self):
        return f"Note for {self.advertiser.name}"

    class Meta:
        db_table = 'advertising_accountnote'  # adjust if your table is named differently
        managed = False  # do not let Django manage this table

class Customer(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sort_1 = models.TextField(null=True, blank=True, db_column='Sort 1')
    sort_2 = models.FloatField(null=True, blank=True, db_column='Sort 2')
    customer_number = models.BigIntegerField(null=True, blank=True, db_column='Customer Number')
    account_number = models.BigIntegerField(null=True, blank=True, db_column='Account Number')
    alt_account_number = models.FloatField(null=True, blank=True, db_column='Alt Account Number')
    first_name = models.TextField(null=True, blank=True, db_column='First Name')
    last_name = models.TextField(null=True, blank=True, db_column='Last Name')
    company_1 = models.TextField(null=True, blank=True, db_column='Company 1')
    company_2 = models.TextField(null=True, blank=True, db_column='Company 2')
    address_1 = models.TextField(null=True, blank=True, db_column='Address 1')
    address_2 = models.TextField(null=True, blank=True, db_column='Address 2')
    city = models.TextField(null=True, blank=True, db_column='City')
    state = models.TextField(null=True, blank=True, db_column='State')
    zip = models.TextField(null=True, blank=True, db_column='Zip')
    country = models.TextField(null=True, blank=True, db_column='Country')
    phone = models.TextField(null=True, blank=True, db_column='Phone')
    email = models.TextField(null=True, blank=True, db_column='Email')
    url = models.TextField(null=True, blank=True, db_column='URL')
    balance = models.TextField(null=True, blank=True, db_column='Balance')
    account_type_code = models.TextField(null=True, blank=True, db_column='Acount Type Code')
    account_type_descr = models.TextField(null=True, blank=True, db_column='Account Type Descr')
    business_unit = models.TextField(null=True, blank=True, db_column='Business Unit')
    salesperson = models.TextField(null=True, blank=True, db_column='Salesperson')
    active = models.BigIntegerField(null=True, blank=True, db_column='Active')
    export_ar = models.BigIntegerField(null=True, blank=True, db_column='Export AR')
    subscriber = models.BigIntegerField(null=True, blank=True, db_column='Subscriber')
    tearsheets = models.BigIntegerField(null=True, blank=True, db_column='Tearsheets')
    credit_limit = models.TextField(null=True, blank=True, db_column='Credit Limit')
    terms = models.TextField(null=True, blank=True, db_column='Terms')
    tax_exempt = models.BigIntegerField(null=True, blank=True, db_column='Tax Exempt')
    tax_id = models.TextField(null=True, blank=True, db_column='Tax ID')
    in_collection = models.BigIntegerField(null=True, blank=True, db_column='In Collection')
    notify_manager = models.BigIntegerField(null=True, blank=True, db_column='Notify Manager')
    do_not_publish = models.BigIntegerField(null=True, blank=True, db_column='Do Not Publish')
    no_new_ads = models.BigIntegerField(null=True, blank=True, db_column='No New Ads')
    setaside_new_ads_code = models.FloatField(null=True, blank=True, db_column='Setaside New Ads Code')
    setaside_new_ads_descr = models.TextField(null=True, blank=True, db_column='Setaside New Ads Descr')
    prepay_required = models.BigIntegerField(null=True, blank=True, db_column='Prepay Required')
    prepay_cash_required = models.BigIntegerField(null=True, blank=True, db_column='Prepay Cash Required')
    po_required = models.BigIntegerField(null=True, blank=True, db_column='PO Required')
    start_date = models.FloatField(null=True, blank=True, db_column='Start Date')
    stop_date = models.FloatField(null=True, blank=True, db_column='Stop Date')
    run_date = models.TextField(null=True, blank=True, db_column='Run Date')
    label_line_1 = models.TextField(null=True, blank=True, db_column='Label Line 1')
    label_line_2 = models.TextField(null=True, blank=True, db_column='Label Line 2')
    label_line_3 = models.TextField(null=True, blank=True, db_column='Label Line 3')
    label_line_4 = models.TextField(null=True, blank=True, db_column='Label Line 4')
    label_line_5 = models.TextField(null=True, blank=True, db_column='Label Line 5')
    label_line_6 = models.TextField(null=True, blank=True, db_column='Label Line 6')

    class Meta:
        db_table = 'advertising_customer'

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

class AdvPubsProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    publication_name = models.CharField(max_length=255)
    country = models.CharField(
        max_length=3,  # ISO 3166-1 Alpha-2 standard for country abbreviations
        default="US"   # Default abbreviation for United States
    )
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)

    class Meta:
        db_table = 'adv_pubs_profile'


class AdvPubsProduct(models.Model):
    PUBLICATION_TYPES = [
        ('magazine', 'Magazine'),
        ('newspaper', 'Newspaper'),
        ('digital', 'Digital'),
    ]

    FOLD_ORIENTATIONS = [
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
        ('none', 'None'),
    ]

    FORMAT_CHOICES = [
        ('jpg', 'JPG'),
        ('png', 'PNG'),
        ('gif', 'GIF'),
        ('mp4', 'MP4'),
        ('none', 'None'),
    ]

    publication = models.ForeignKey('AdvPubsProfile', on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=20, choices=PUBLICATION_TYPES)
    name = models.TextField()
    measurement_unit = models.CharField(max_length=10, choices=[('inch', 'Inch'), ('cm', 'CM'), ('pixel', 'Pixel')], null=True, blank=True)
    fold_orientation = models.CharField(max_length=10, choices=FOLD_ORIENTATIONS, default='none')
    formats = models.CharField(max_length=100, default='none')  # Use CharField to simulate SET behavior
    width = models.IntegerField()
    height = models.IntegerField()
    active = models.BooleanField(default=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'adv_pubs_products'

    def __str__(self):
        return self.name

