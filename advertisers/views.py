from django.shortcuts import render, redirect, get_object_or_404
from adCampaigns.models import Account, CompanyContact, AccountNote, AccountType, SalesPerson, IndustryCode
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils.timezone import now

def index(request):
  advertiser_list = Account.objects.all().order_by('-created_at')
  paginator = Paginator(advertiser_list, 10) 
  
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, 'advertisers/allAdvertisers.html', {
      'page_obj': page_obj
  })

def advertiser(request, id):
  advertiser = get_object_or_404(Account, id=id)

  if request.method == 'POST':
    note_text = request.POST.get("note", "").strip()
    user = request.user.username if request.user.is_authenticated else "Anonymous"

    if note_text:
        AccountNote.objects.create(
            note=note_text,
            timestamp=now(),
            updatedAt=now(),
            account_id=id,
            user=user
        )
        return redirect('advertiser', id=id)  # refresh after POST

  contacts = CompanyContact.objects.filter(account_id=id)
  notes = AccountNote.objects.filter(account_id=id).order_by('-timestamp')
  return render(request, 'advertisers/singleAdvertiser.html', {
    'advertiser': advertiser,
    'contacts': contacts,
    'notes': notes

  })


def createAdvertiser(request):
    account_types = AccountType.objects.all()
    sales_persons = SalesPerson.objects.all()
    industry_codes = IndustryCode.objects.all()

    if request.method == 'POST':
        # Contact Info
        contact_name_first = request.POST.get('advertiser_firstname', '').strip()
        contact_name_last = request.POST.get('advertiser_lastname', '').strip()
        contact_full_name = f"{contact_name_first} {contact_name_last}".strip()
        phone = request.POST.get('advertiser_phone', '').strip()
        email = request.POST.get('advertiser_email', '').strip()

        # Business Info
        company_name_1 = request.POST.get('business_name', '').strip()
        address = request.POST.get('advertiser_address', '').strip()
        city = request.POST.get('advertiser_city', '').strip()
        state = request.POST.get('advertiser_state', '').strip()
        zip_code = request.POST.get('advertiser_zipcode', '').strip()
        website = request.POST.get('advertiser_website', '').strip()
        billing_email = request.POST.get('advertiser_billing_email', '').strip()
        legacy_id = request.POST.get('advertiser_legacy_id', '').strip()

        # Related FK dropdowns
        account_type = AccountType.objects.filter(id=request.POST.get('advertiser_account_type')).first()
        sales_person = SalesPerson.objects.filter(id=request.POST.get('sales-person')).first()
        industry_code = IndustryCode.objects.filter(id=request.POST.get('advertiser_industry_code')).first()

        # Billing address logic
        if request.POST.get('billing_option') == 'different':
            billing_address = request.POST.get('billing_address', '').strip()
            billing_city = request.POST.get('billing_city', '').strip()
            billing_state = request.POST.get('billing_state', '').strip()
            billing_zip = request.POST.get('billing_zipcode', '').strip()
        else:
            billing_address = address
            billing_city = city
            billing_state = state
            billing_zip = zip_code

        # Create Account
        new_account = Account.objects.create(
            name=company_name_1,
            contact_name=contact_full_name,
            contact_name_first=contact_name_first,
            contact_name_last=contact_name_last,
            phone=phone,
            email=email,
            company_name_1=company_name_1,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            website=website,
            billing_email=billing_email,
            legacy_id=legacy_id,
            billing_address=billing_address,
            billing_city=billing_city,
            billing_state=billing_state,
            billing_zip_code=billing_zip,
            account_type=account_type,
            sales_person=sales_person,
            industry_code=industry_code
        )

        return JsonResponse({'success': True, 'advertiser_id': new_account.id})
        # Make sure this matches your URLconf

    return render(request, 'advertisers/createAdvertiser.html', {
        'account_types': account_types,
        'sales_persons': sales_persons,
        'industry_codes': industry_codes,
    })

@csrf_exempt
def add_contact(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)

        contact = CompanyContact.objects.create(
            account_id=id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            full_name=f"{data.get('first_name', '')} {data.get('last_name', '')}",
            email=data.get('email'),
            department_id=1,
            default=1 if data.get('is_primary') else 0,
            active=1
        )


        return JsonResponse({'success': True, 'contact_id': contact.id})

    return JsonResponse({'error': 'Invalid method'}, status=400)

@csrf_exempt
def add_notes_to_advertiser(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notes = data.get('notes', [])
            advertiser = Account.objects.get(id=id)

            for note in notes:
                AccountNote.objects.create(
                    account=advertiser,
                    note=note.get('text', ''),
                    timestamp=now(),
                    user=request.user if request.user.is_authenticated else None
                )

            return JsonResponse({'success': True, 'message': 'Notes saved.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)