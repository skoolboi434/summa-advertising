from django.shortcuts import render, redirect
from .models import Role, Region, Rate, Status, AccountType, Publication, Account, AdvPubsProduct, CompanyInfo, AdminAdType, MarketCode, AdCriteria
from classifieds.models import Classification
from users.models import AdvertisingUser
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone



def index(request):
  return render(request, 'admin/portal.html')

from django.shortcuts import redirect

def adminGeneral(request):
    if request.method == "POST":
        name = request.POST.get("region-name")
        code = request.POST.get("region-code")
        publications = request.POST.getlist("publications")  # list of IDs

        region = Region.objects.create(
            name=name,
            code=code,
            status="active",  # or whatever you want as default
            created_by=request.user 
        )
        if publications:
            region.publications.set(publications)  # save M2M relation

        if request.method == "POST":
            publications = request.POST.getlist("publications")
            print("DEBUG publications:", publications)


        return redirect("adminGeneral")  # redirect to same page after submit

    publications = Publication.objects.all()
    advertiser_list = Account.objects.all().order_by('-created_at')
    regions = Region.objects.all().order_by('-created_at')
    regions_paginator = Paginator(regions, 10)
    region_page_number = request.GET.get('page')
    regions_page_obj = regions_paginator.get_page(region_page_number)
    

    products = AdvPubsProduct.objects.all()
    products_paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = products_paginator.get_page(page_number)
    company = CompanyInfo.objects.first() 

    return render(request, 'admin/general.html', {
        'publications': publications,
        'advertiser_list': advertiser_list,
        'regions': regions,
        'page_obj': page_obj,
        "company": company,
        "regions_page_obj": regions_page_obj,
    })


# Admin Products
def newMagazine(request):
  return render(request, 'admin/includes/general/newMagazine.html')

def adminPubSetup(request):
  return render(request, 'admin/pubs/newPublication.html')

def adminAds(request):
    if request.method == "POST":
        # Determine which form was submitted
        if "ad-type-name" in request.POST:
            # Admin Ad Type form
            name = request.POST.get("ad-type-name")
            code = request.POST.get("ad-type-code")
            default_rate_id = request.POST.get("ad-type-rate")
            publications = request.POST.getlist("publications")  # list of IDs

            adType = AdminAdType.objects.create(
                name=name,
                code=code,
                status="active",
                default_rate_id=default_rate_id or None,
                created_by=request.user
            )
            if publications:
                adType.publications.set(publications)
            return redirect("adminAds")

        elif "market-code-name" in request.POST:
            # Market Code form
            name = request.POST.get("market-code-name")
            code = request.POST.get("market-code")

            marketCode = MarketCode.objects.create(
                name=name,
                code=code,
                status="active",
                created_by=request.user
            )
        
        elif "adCriteria-name" in request.POST:
            # Market Code form
            name = request.POST.get("adCriteria-name")
            code = request.POST.get("adCriteria-code")
            publications = request.POST.getlist("publications")

            adCriteria = AdCriteria.objects.create(
                name=name,
                code=code,
                status="active",
                created_by=request.user
            )
            if publications:
                adCriteria.publications.set(publications)
            return redirect("adminAds")

        

    # GET request
    adTypes = AdminAdType.objects.all().order_by('-created_at')
    adTypes_paginator = Paginator(adTypes, 10)
    adType_page_number = request.GET.get('page')
    adTypes_page_obj = adTypes_paginator.get_page(adType_page_number)

    marketCodes = MarketCode.objects.all().order_by('-created_at')
    marketCodes_paginator = Paginator(marketCodes, 10)
    marketCode_page_number = request.GET.get('page')
    marketCodes_page_obj = marketCodes_paginator.get_page(marketCode_page_number)

    adCriterias = AdCriteria.objects.all().order_by('-created_at')
    adCriterias_paginator = Paginator(adCriterias, 10)
    adCriteria_page_number = request.GET.get('page')
    adCriterias_page_obj = adCriterias_paginator.get_page(adCriteria_page_number)

    publications = Publication.objects.all()
    rates = Rate.objects.all()

    return render(request, 'admin/ads.html', {
        'publications': publications,
        'rates': rates,
        'adTypes': adTypes,
        'marketCodes': marketCodes,
        "adTypes_page_obj": adTypes_page_obj,
        "marketCodes_page_obj": marketCodes_page_obj,
        "adCriterias_page_obj": adCriterias_page_obj,
    })


def adminFinancial(request):
  return render(request, 'admin/financial.html')

def adminPricing(request):
  return render(request, 'admin/pricing.html')

# Admin Account Routes

def adminAccounts(request):
    accountTypes = AccountType.objects.all().order_by('-id')
    users = AdvertisingUser.objects.all().order_by('-id')
    roles = Role.objects.all().order_by('-id')
    paginator = Paginator(accountTypes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    statuses = Status.objects.all()
    if request.method == 'POST':
        print("📨 POST request received")
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()
        status_id = request.POST.get('status')

        print(f"📥 Form values - name: '{name}', code: '{code}', status: '{status_id}'")

        status_obj = Status.objects.filter(id=status_id).first()

        if name and code and status_id:
            status_obj = Status.objects.filter(id=status_id).first()
            new_type = AccountType.objects.create(name=name, code=code, status=status_obj)
            print("✅ Created new AccountType:", new_type.id, new_type.name)
            return redirect('adminAccounts')
        else:
            print("⚠️ Name or code missing. Not creating.")
    
    can_edit_account_type = request.user.has_perm('adAdmin.change_accounttype')
    can_delete_account_type = request.user.has_perm('adAdmin.delete_accounttype')

    return render(request, 'admin/accounts.html', {
        'page_obj': page_obj,
        'roles': roles,
        'statuses': statuses,
        'users': users,
        'can_edit_account_type': can_edit_account_type,
        'can_delete_account_type': can_delete_account_type,
    })

def createUser(request):
    roles = Role.objects.all()
    regions = Region.objects.all()
    publications = Publication.objects.all()
    accountTypes = AccountType.objects.all().order_by('-id')
    statuses = Status.objects.all().order_by('name')

    if request.method == 'POST':
        data = request.POST

        user = AdvertisingUser.objects.create(
            first_name=data.get('first_name', '').strip(),
            last_name=data.get('last_name', '').strip(),
            username=data.get('username', '').strip(),
            nickname=data.get('nickname', '').strip() or None,
            email=data.get('email', '').strip(),
            phone=data.get('phone', '').strip() or None,
            website=data.get('website', '').strip() or None,
            bio=data.get('bio', '').strip() or None,
            language=data.get('language', '').strip() or None,
            status_id=data.get('status') or None,
            region_id=data.get('region') or None,
            role_id=data.get('role') or None,
            commission=data.get('commission') or 0.0,
            created_at=now(),
            updated_at=now(),
        )
        return redirect(reverse('userProfile', kwargs={'id': user.id}))

    return render(request, 'users/createUser.html', {
        'statuses': statuses,
        'roles': roles,
        'regions': regions,
        'publications': publications,
        'accountTypes': accountTypes
    })

def adminClassifieds(request):
    classification_list = Classification.objects.all()
    category_paginator = Paginator(classification_list, 15)

    page_number = request.GET.get('page')
    page_obj = category_paginator.get_page(page_number)

    return render(request, 'admin/classifieds.html', {'page_obj': page_obj})

def createAdminStyle(request):

    return render(request, 'admin/includes/classifieds/createAdminStyle.html')