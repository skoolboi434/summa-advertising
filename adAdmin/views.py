from django.shortcuts import render, redirect, get_object_or_404
from .models import Role, Region, Rate, Status, AccountType, Publication, Account, AdvPubsProduct, CompanyInfo, AdminAdType, MarketCode, AdCriteria, Section, AdminAdjustment, GLCode, RateGroup, AdminTax, FiscalYear, RateGroup, StandardSize, NewspaperProduct, MagazineProduct, DigitalProduct
from classifieds.models import Classification, ClassifiedUpsell, ClassifiedAddon, ClassifiedMeasurement
from users.models import AdvertisingUser
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.http import JsonResponse
login_redirect = "/accounts/login"


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

    magazines = MagazineProduct.objects.all().order_by('-created_at')
    magazines_paginator = Paginator(magazines, 10)
    magazine_page_number = request.GET.get('page')
    magazines_page_obj = magazines_paginator.get_page(magazine_page_number)
    
    newspapers = NewspaperProduct.objects.all().order_by('-created_at')
    newspapers_paginator = Paginator(newspapers, 10)
    newspaper_page_number = request.GET.get('page')
    newspapers_page_obj = newspapers_paginator.get_page(newspaper_page_number)

    digitals = DigitalProduct.objects.all().order_by('-created_at')
    digitals_paginator = Paginator(digitals, 10)
    digital_page_number = request.GET.get('page')
    digitals_page_obj = digitals_paginator.get_page(digital_page_number)
    
    products = AdvPubsProduct.objects.all().order_by('-created_at')
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
        'newspapers_page_obj': newspapers_page_obj,
        'magazines_page_obj': magazines_page_obj,
        "digitals_page_obj": digitals_page_obj
        
    })


# Admin Products
def add_standardsize(request):
    if request.method == "POST":
        data = json.loads(request.body)
        size = StandardSize.objects.create(
            description=data.get("description"),
            height=data.get("height"),
            columns=data.get("columns"),
            type=2,  # or whatever type you want
        )
        return JsonResponse({
            "id": size.id,
            "description": size.description,
            "height": size.height,
            "columns": size.columns
        })


    return JsonResponse({"error": "Invalid request method"}, status=405)

def newMagazine(request):
    # --- Handle AJAX JSON POST for creating sizes (not product) ---
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Invalid JSON: {e}"}, status=400)

        # ✅ Create new StandardSize
        try:
            size = StandardSize.objects.create(
                description=data.get("description"),
                height=data.get("height"),
                columns=data.get("columns"),
            )
            return JsonResponse({
                "id": size.id,
                "description": size.description,
                "height": size.height,
                "columns": size.columns,
                "created_at": size.created_at.strftime("%Y-%m-%d %H:%M"),
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    # --- Handle normal product creation form ---
    if request.method == "POST":
        magazine = MagazineProduct.objects.create(
            product_mag=request.POST.get("product-mag"),
            measurement_type=request.POST.get("measurement-type"),
            fold_orientation=request.POST.get("fold-orientation"),
            height=request.POST.get("height") or 0,
            width=request.POST.get("width") or 0,
            columns=request.POST.get("columns-per-page") or 0,
            column_width=request.POST.get("column-width") or 0,
            page_width=request.POST.get("page_width") or 0,
            page_height=request.POST.get("page_height") or 0,
            page_border=request.POST.get("page_border") or 0,
            gutter_size=request.POST.get("gutter_size") or 0,
            active=request.POST.get("active") == "on",
        )

        # Attach selected StandardSizes
        selected_sizes = request.POST.getlist("sizes")
        if selected_sizes:
            magazine.sizes.set(selected_sizes)  # ✅ directly link M2M

        return redirect("adminGeneral")
      # 👈 send them somewhere after save

    # --- GET: Render form ---
    standardsizes = StandardSize.objects.all().order_by("-created_at")
    standardsizes_paginator = Paginator(standardsizes, 8)
    standardsize_page_number = request.GET.get("page")
    standardsizes_page_obj = standardsizes_paginator.get_page(standardsize_page_number)

    return render(request, "admin/includes/general/newMagazine.html", {
        "standardsizes_page_obj": standardsizes_page_obj
    })




def newNewspaper(request):
    # --- Handle AJAX JSON POST for creating sizes (not product) ---
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Invalid JSON: {e}"}, status=400)

        # ✅ Create new StandardSize
        try:
            size = StandardSize.objects.create(
                description=data.get("description"),
                height=data.get("height"),
                columns=data.get("columns"),
            )
            return JsonResponse({
                "id": size.id,
                "description": size.description,
                "height": size.height,
                "columns": size.columns,
                "created_at": size.created_at.strftime("%Y-%m-%d %H:%M"),
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    # --- Handle normal product creation form ---
    if request.method == "POST":
        newspaper = NewspaperProduct.objects.create(
            product_newspaper=request.POST.get("newspaper-product"),
            measurement_type=request.POST.get("measurement-type"),
            fold_orientation=request.POST.get("fold-orientation"),
            height=request.POST.get("height") or 0,
            width=request.POST.get("width") or 0,
            columns=request.POST.get("columns-per-page") or 0,
            column_width=request.POST.get("column-width") or 0,
            page_width=request.POST.get("page_width") or 0,
            page_height=request.POST.get("page_height") or 0,
            page_border=request.POST.get("page_border") or 0,
            gutter_size=request.POST.get("gutter_size") or 0,
            active=request.POST.get("active") == "on",
        )

        # Attach selected StandardSizes
        selected_sizes = request.POST.getlist("sizes")
        if selected_sizes:
            newspaper.sizes.set(selected_sizes)  # ✅ directly link M2M

        return redirect("adminGeneral")
      # 👈 send them somewhere after save

    # --- GET: Render form ---
    standardsizes = StandardSize.objects.all().order_by("-created_at")
    standardsizes_paginator = Paginator(standardsizes, 8)
    standardsize_page_number = request.GET.get("page")
    standardsizes_page_obj = standardsizes_paginator.get_page(standardsize_page_number)

    return render(request, "admin/includes/general/newNewspaper.html", {
        "standardsizes_page_obj": standardsizes_page_obj
    })

def newDigital(request):
    # --- Handle AJAX JSON POST for creating sizes (not product) ---
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Invalid JSON: {e}"}, status=400)

        # ✅ Create new StandardSize
        try:
            size = StandardSize.objects.create(
                description=data.get("description"),
                height=data.get("height"),
                columns=data.get("columns"),
            )
            return JsonResponse({
                "id": size.id,
                "description": size.description,
                "height": size.height,
                "columns": size.columns,
                "created_at": size.created_at.strftime("%Y-%m-%d %H:%M"),
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    # --- Handle normal product creation form ---
    if request.method == "POST":
        selected_ad_type_id = request.POST.get("ad-type")
        selected_ad_type = AdminAdType.objects.get(id=selected_ad_type_id)

        digital = DigitalProduct.objects.create(
            product_mag=request.POST.get("product-mag"),   # ✅ match your form field
            format=request.POST.get("format"),
            height=request.POST.get("height") or 0,
            width=request.POST.get("width") or 0,
            adminadtype=selected_ad_type,   # ✅ assign FK object
            active=request.POST.get("active") == "on",
        )

        # Attach selected StandardSizes
        selected_sizes = request.POST.getlist("sizes")
        if selected_sizes:
            digital.sizes.set(selected_sizes)  # ✅ correct model reference

        return redirect("adminGeneral")  # 👈 adjust redirect if needed

    # --- GET: Render form ---
    standardsizes = StandardSize.objects.all().order_by("-created_at")
    standardsizes_paginator = Paginator(standardsizes, 8)
    standardsize_page_number = request.GET.get("page")
    standardsizes_page_obj = standardsizes_paginator.get_page(standardsize_page_number)

    adTypes = AdminAdType.objects.all()

    return render(request, "admin/includes/general/newDigital.html", {
        "standardsizes_page_obj": standardsizes_page_obj,
        "adTypes": adTypes,
    })

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
            return redirect("adminAds")

        elif "section-name" in request.POST:
            # Market Code form
            name = request.POST.get("section-name")
            code = request.POST.get("section-code")
            sub_section = request.POST.get("ad-sub-section")
            publications = request.POST.getlist("publications")

            section = Section.objects.create(
                name=name,
                code=code,
                sub_section=sub_section,
                status="active",
                created_by=request.user
            )
            if publications:
                section.publications.set(publications)
            return redirect("adminAds")
        
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

    sections = Section.objects.all().order_by('-created_at')
    sections_paginator = Paginator(sections, 10)
    section_page_number = request.GET.get('page')
    sections_page_obj = sections_paginator.get_page(section_page_number)

    adCriterias = AdCriteria.objects.all().order_by('-created_at')
    adCriterias_paginator = Paginator(adCriterias, 10)
    adCriteria_page_number = request.GET.get('page')
    adCriterias_page_obj = adCriterias_paginator.get_page(adCriteria_page_number)

    publications = Publication.objects.all()
    rates = Rate.objects.all()

    return render(request, 'admin/ads.html', {
        'publications': publications,
        'rates': rates,
        "adTypes_page_obj": adTypes_page_obj,
        "marketCodes_page_obj": marketCodes_page_obj,
        "adCriterias_page_obj": adCriterias_page_obj,
        "sections_page_obj": sections_page_obj,
    })


def adminFinancial(request):
  if request.method == "POST":
      # Determine which form was submitted
          if "fiscal-year-name" in request.POST:
            name = request.POST.get("fiscal-year-name")
            startDate = request.POST.get("fiscal-year-start-date")
            endDate = request.POST.get("fiscal-year-end-date")

            # Create Fiscal Year
            fiscalYear = FiscalYear.objects.create(
                name=name,
                startDate=startDate,
                endDate=endDate,
                status="active",
                created_by=request.user
            )

            return redirect("adminFinancial")

          elif "glcode-code" in request.POST:
            # Market Code form
            code = request.POST.get("glcode-code")
            code_type = request.POST.get("glcode-type")
            description = request.POST.get("glcode-description")

            glCode = GLCode.objects.create(
                code=code,
                code_type=code_type,
                description=description,
                status="active",
                created_by=request.user
            )
            return redirect("adminFinancial")
  
  fiscalYears = FiscalYear.objects.all().order_by('-created_at')
  fiscalYears_paginator = Paginator(fiscalYears, 10)
  fiscalYear_page_number = request.GET.get('page')
  fiscalYears_page_obj = fiscalYears_paginator.get_page(fiscalYear_page_number)

  glCodes = GLCode.objects.all().order_by('-date_created')

  return render(request, 'admin/financial.html', {
    "fiscalYears_page_obj":fiscalYears_page_obj,
    "glCodes":glCodes,
  })

def adminPricing(request):
  if request.method == "POST":
      # Determine which form was submitted
          if "adjustment-name" in request.POST:
            name = request.POST.get("adjustment-name")
            code = request.POST.get("adjustment-code")
            apply_level = request.POST.get("adjustment-apply-level")
            section_id = request.POST.get("adjustment-section")
            value_type = request.POST.get("adjustment-value-type")
            value = request.POST.get("adjustment-value")
            prompt_for_value = request.POST.get("value-prompt")
            type = request.POST.get("adjustment-pay-type")
            gl_code_id = request.POST.get("adjustment-assigned-gl")

            # Resolve FK instances
            section_instance = Section.objects.get(id=section_id) if section_id else None
            gl_code_instance = GLCode.objects.get(id=gl_code_id) if gl_code_id else None

            # Create adjustment
            adjustment = AdminAdjustment.objects.create(
                name=name,
                code=code,
                apply_level=apply_level,
                section=section_instance,
                value_type=value_type,
                value=float(value or 0),
                prompt_for_value=(prompt_for_value == "on"),
                type=type,
                gl_code=gl_code_instance,
                status="active",
                created_by=request.user
            )

            # Many-to-Many: multiple GL codes
            glCodes = request.POST.getlist("glCodes")
            if glCodes:
                glCodes = [int(gid) for gid in glCodes]  # ensure integers
                adjustment.glCodes.set(glCodes)

            # Many-to-Many: publications
            publications = request.POST.getlist("publications")
            if publications:
                publications = [int(pid) for pid in publications]
                adjustment.publications.set(publications)

            return redirect("adminPricing")

          elif "tax-name" in request.POST:
            # Market Code form
            name = request.POST.get("tax-name")
            description = request.POST.get("tax-description")
            start_date = request.POST.get("tax-start-date")
            end_date = request.POST.get("tax-end-date")
            amount = request.POST.get("tax-amount")
            format = request.POST.get("taxFormat")
            assigned_gl = request.POST.get("taxGLAssign")
            gl_code_id = request.POST.get("tax-gl-code")  # replace with the correct input name
            gl_code_instance = GLCode.objects.get(id=gl_code_id) if gl_code_id else None

            adTax = AdminTax.objects.create(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                amount=amount,
                format=format,
                assigned_gl=assigned_gl,
                gl_code=gl_code_instance,
                status="active",
                created_by=request.user
            )

            glCodes = request.POST.getlist("glCodes")
            if glCodes:
                glCodes = [int(gid) for gid in glCodes]  # ensure integers
                adTax.glCodes.set(glCodes)
            return redirect("adminPricing")
          
          elif "rate-group-name" in request.POST:
            # Market Code form
            name = request.POST.get("rate-group-name")
            description = request.POST.get("rate-group-description")

            rateGroup = RateGroup.objects.create(
                name=name,
                description=description,
                status="active",
                created_by=request.user
            )

            # Many-to-Many: publications
            publications = request.POST.getlist("publications")
            if publications:
                publications = [int(pid) for pid in publications]
                rateGroup.publications.set(publications)
                
            return redirect("adminPricing")

          elif "rate-name" in request.POST:
            name = request.POST.get("rate-name")
            measurement_type = request.POST.get("ad-criteria")
            pricing = request.POST.get("isPricing")
            
            # Handle tax safely
            tax_category_id = request.POST.get("tax-category")
            if tax_category_id:
                tax_name = AdminTax.objects.get(id=tax_category_id).name
            else:
                tax_name = ""
            
            override_privileges = request.POST.get("overridePriveledges")
            assigned_groups = request.POST.get("rateGroupAssign") == "true"
            start_date = request.POST.get("rate-start-date")
            end_date = request.POST.get("rate-end-date") or None
            description = request.POST.get("rate-description")

            # Shared computation fields
            insertion_min = (
                request.POST.get("lines-min")
                or request.POST.get("words-min")
                or request.POST.get("units-min")
            )
            insertion_max = (
                request.POST.get("lines-max")
                or request.POST.get("words-max")
                or request.POST.get("units-max")
            )
            base_cost = (
                request.POST.get("lines-base-cost")
                or request.POST.get("words-base-cost")
                or request.POST.get("units-base-cost")
            )
            base_count = (
                request.POST.get("lines-num-of-lines")
                or request.POST.get("words-num-of-words")
                or request.POST.get("units-num-of-units")
            )
            additional_cost = request.POST.get("extra-charge")
            additional_count = (
                request.POST.get("lines-extra-charge-num-of-lines")
                or request.POST.get("words-extra-charge-num-of-words")
                or request.POST.get("units-extra-charge-num-of-units")
            )

            charge_for = (
                request.POST.get("linesChargeFor")
                or request.POST.get("wordsChargeFor")
                or request.POST.get("unitsChargeFor")
            )

            # Create Rate safely
            rate = Rate.objects.create(
                name=name,
                pricing=pricing,
                measurement_type=measurement_type,
                tax_category=tax_name,  # <-- safe, can be None
                override_privileges=override_privileges,
                assigned_groups=assigned_groups,
                start_date=start_date,
                end_date=end_date,
                description=description,
                insertion_min=insertion_min or "0",
                insertion_max=insertion_max or "0",
                base_cost=base_cost or "0",
                base_count=base_count or "0",
                additional_cost=additional_cost or "0",
                additional_count=additional_count or "0",
                charge_for=charge_for,
                created_by=request.user,
            )


            # Type-specific detail models
            # if measurement_type == "inches":
            #     InchesRateDetail.objects.create(
            #         rate=rate,
            #         default_cost_per_col_inch=request.POST.get("inches-width", 0),
            #         height=request.POST.get("inches-height", 0),
            #     )

            # elif measurement_type == "digital":
            #     DigitalRateDetail.objects.create(
            #         rate=rate,
            #         impressions=request.POST.get("digital-impressions", 0),
            #         clicks=request.POST.get("digital-clicks", 0),
            #     )



  adjustments = AdminAdjustment.objects.all().order_by('-date_created')
  adjustments_paginator = Paginator(adjustments, 10)
  adjustment_page_number = request.GET.get('page')
  adjustments_page_obj = adjustments_paginator.get_page(adjustment_page_number)

  rateGroups = RateGroup.objects.all().order_by('-created_at')
  rateGroups_paginator = Paginator(rateGroups, 10)
  rateGroup_page_number = request.GET.get('page')
  rateGroups_page_obj = rateGroups_paginator.get_page(rateGroup_page_number)

  adminTaxes = AdminTax.objects.all().order_by('-created_at')
  adminTaxes_paginator = Paginator(adminTaxes, 10)
  adminTax_page_number = request.GET.get('page')
  adminTaxes_page_obj = adminTaxes_paginator.get_page(adminTax_page_number)

  rates = Rate.objects.all().order_by('-created_at')
  rates_paginator = Paginator(rates, 10)
  rate_page_number = request.GET.get('page')
  rates_page_obj = rates_paginator.get_page(rate_page_number)

  publications = Publication.objects.all()
  glCodes = GLCode.objects.all()
  

  return render(request, 'admin/pricing.html', {
    'adjustments_page_obj': adjustments_page_obj,
    'publications': publications,
    'adminTaxes_page_obj': adminTaxes_page_obj,
    'glCodes': glCodes,
    'rateGroups_page_obj': rateGroups_page_obj,
    "rates_page_obj": rates_page_obj,
  })

def singleRateGroup(request, id):
  rateGroup = get_object_or_404(RateGroup, id=id)
  return render(request, 'admin/includes/pricing/singleRateGroup.html', {
    'rateGroup': rateGroup,

  })

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
    if request.method == "POST":
        if "category-name" in request.POST:
            name = request.POST.get("category-name")
            self_service = request.POST.get("selfService")
            is_subcategory = request.POST.get("isSubcategory")
            assigned_gl = request.POST.get("isGl-override")
            gl_code_id = request.POST.get("category-override-gl")

            gl_code_instance = GLCode.objects.get(id=gl_code_id) if gl_code_id else None
            main_category_id = request.POST.get("main-category-select")
            parent_instance = Classification.objects.get(id=main_category_id) if main_category_id else None

            classification = Classification.objects.create(
                name=name,
                self_service=self_service,
                is_subcategory=is_subcategory,
                assigned_gl=assigned_gl,
                status="active",
                parent=parent_instance
            )


            # Many-to-Many: GL Codes
            glCodes = request.POST.getlist("glCodes")
            if glCodes:
                glCodes = [int(gid) for gid in glCodes]  # ensure integers
                classification.glCodes.set(glCodes)      # <-- FIXED

            # Many-to-Many: Publications
            publications = request.POST.getlist("publications")
            if publications:
                publications = [int(pid) for pid in publications]
                classification.publications.set(publications)  # <-- FIXED

            return redirect("adminClassifieds")

        elif "upsell-name" in request.POST:
          # Market Code form
          name = request.POST.get("upsell-name")
          description = request.POST.get("upsell-description")

          # Assigned Rate radio
          assigned_rate = request.POST.get("isAssignedRate")  # "default" or "override"

          # GL override radio
          gl_override_mode = request.POST.get("isGlOverride")  # "default" or "override"

          assigned_gl = gl_override_mode

          self_service = request.POST.get("upsell-self-service")

          # Create upsell record
          upsell = ClassifiedUpsell.objects.create(
              name=name,
              description=description,
              assigned_rate=assigned_rate,   # store correct value
              assigned_gl=assigned_gl,
              self_service=self_service,
              status="active",
              created_by=request.user,
          )

          # Attach GL codes only if override is selected
          if gl_override_mode == "override":
              glCodes = request.POST.getlist("upsell-override-gl")
              if glCodes:
                  glCodes = [int(gid) for gid in glCodes]  # ensure integers
                  upsell.glCodes.set(glCodes)

          # Attach publications
          publications = request.POST.getlist("publications")
          if publications:
              publications = [int(pid) for pid in publications]
              upsell.publications.set(publications)

          return redirect("adminClassifieds")

        elif "addon-name" in request.POST:
          # Market Code form
          name = request.POST.get("addon-name")
          description = request.POST.get("addon-description")
          self_service = request.POST.get("addon-self-service")
          price = request.POST.get("addon-pricing")

          # Create upsell record
          addon = ClassifiedAddon.objects.create(
              name=name,
              description=description,
              self_service=self_service,
              price=price,
              status="active",
              created_by=request.user,
          )


          # Attach publications
          publications = request.POST.getlist("publications")
          if publications:
              publications = [int(pid) for pid in publications]
              addon.publications.set(publications)

          return redirect("adminClassifieds")

        elif "measurement-name" in request.POST:
          # Market Code form
          name = request.POST.get("measurement-name")
          orientation = request.POST.get("fold-orientation")
          width = request.POST.get("measurement-width")
          height = request.POST.get("measurement-height")
          page_columns = request.POST.get("columns-per-page")
          column_width = request.POST.get("column-width")
          page_width = request.POST.get("page-width")
          page_height = request.POST.get("page-height")
          page_border = request.POST.get("page-border")
          gutter_size = request.POST.get("gutter-size")
          self_service = request.POST.get("measurement-selfService")
          price = request.POST.get("addon-pricing")

          # Create measurement record
          measurement = ClassifiedMeasurement.objects.create(
              name=name,
              orientation=orientation,
              width=width,
              height=height,
              page_columns=page_columns,
              column_width=column_width,
              page_width=page_width,
              page_height=page_height,
              page_border=page_border,
              gutter_size=gutter_size,
              self_service=self_service,
              status="active",
              created_by=request.user,
          )


          # Attach publications
          publications = request.POST.getlist("publications")
          if publications:
              publications = [int(pid) for pid in publications]
              measurement.publications.set(publications)

          return redirect("adminClassifieds")



    glCodes = GLCode.objects.all()
    publications = Publication.objects.all()
    classifications_select = Classification.objects.all().order_by('-created_at')

    classifications = Classification.objects.all().order_by('-created_at')
    classifications_paginator = Paginator(classifications, 10)
    classification_page_number = request.GET.get('page')
    classifications_page_obj = classifications_paginator.get_page(classification_page_number)

    measurements = ClassifiedMeasurement.objects.all().order_by('-created_at')
    measurements_paginator = Paginator(measurements, 10)
    measurement_page_number = request.GET.get('page')
    measurements_page_obj = measurements_paginator.get_page(measurement_page_number)

    upsells = ClassifiedUpsell.objects.all().order_by('-created_at')
    upsells_paginator = Paginator(upsells, 10)
    upsell_page_number = request.GET.get('page')
    upsells_page_obj = upsells_paginator.get_page(classification_page_number)

    addons = ClassifiedMeasurement.objects.all().order_by('-created_at')
    addons_paginator = Paginator(addons, 10)
    addon_page_number = request.GET.get('page')
    addons_page_obj = addons_paginator.get_page(classification_page_number)

    return render(request, 'admin/classifieds.html', {
        'classifications_page_obj': classifications_page_obj,
        'upsells_page_obj': upsells_page_obj,
        'addons_page_obj': addons_page_obj,
        'measurements_page_obj': measurements_page_obj,
        'glCodes': glCodes,
        'publications': publications,
        'classifications_select': classifications_select
    })

def createAdminStyle(request):

    return render(request, 'admin/includes/classifieds/createAdminStyle.html')