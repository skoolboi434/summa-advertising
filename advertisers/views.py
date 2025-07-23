from django.shortcuts import render, redirect, get_object_or_404
from adCampaigns.models import Account, CompanyContact, AccountNote, AccountType, SalesPerson, IndustryCode
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils.timezone import now

def index(request):
  advertiser_list = Account.objects.all().order_by('name')
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
  return render(request, 'advertisers/createAdvertiser.html', {'account_types': account_types, 'sales_persons': sales_persons, 'industry_codes': industry_codes})

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