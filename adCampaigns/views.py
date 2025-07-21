from django.shortcuts import render, redirect, get_object_or_404
from .models import AdvertisingCampaignSummary, SalesPerson, Account
from django.db.models import Q
from django.http import JsonResponse
from .forms import AdCampaignForm
import json
from django.utils.timezone import now
from django.db import connection

def generate_new_campaign_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(id) FROM advertising_campaign_summary")
        row = cursor.fetchone()
        return (row[0] or 0) + 1


def index(request):
    campaigns = AdvertisingCampaignSummary.objects.all()
    return render(request, 'adCampaigns/allCampaigns.html', {
        'campaigns': campaigns
    })


def createCampaign(request):
    if request.method == 'POST':
        form = AdCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)

            # Advertiser
            advertiser_id = request.POST.get("advertiser_id")
            if advertiser_id:
                campaign.advertiser_id = int(advertiser_id)
                advertiser_obj = Account.objects.filter(id=advertiser_id).first()
                campaign.advertiser_name = advertiser_obj.name if advertiser_obj else ''
            else:
                campaign.advertiser_id = None
                campaign.advertiser_name = ''

            # Sales Contact
            contact_id = request.POST.get("contact_id")
            if contact_id:
                campaign.contact_id = int(contact_id)
                contact = SalesPerson.objects.filter(id=contact_id).first()
                campaign.sales_contact = contact.first_name if contact else ''
            else:
                campaign.contact_id = None
                campaign.sales_contact = ''

            # Save
            campaign.id = generate_new_campaign_id()
            campaign.total_sub = 0
            campaign.total_adjustment = 0
            campaign.total_campaign = 0

            campaign.save()

            # ✅ Define before render
            contacts = SalesPerson.objects.all()
            accounts = Account.objects.all()

            return render(request, 'adCampaigns/createAdCampaign.html', {
                'form': AdCampaignForm(),  # reset form
                'contacts': contacts,
                'accounts': accounts,
                'success': True,
                'campaign_id': campaign.id
            })

        else:
            print("Form invalid:", form.errors)

            contacts = SalesPerson.objects.all()
            accounts = Account.objects.all()

            return render(request, 'adCampaigns/createAdCampaign.html', {
                'form': form,
                'contacts': contacts,
                'accounts': accounts,
            })

    else:
        form = AdCampaignForm()

    contacts = SalesPerson.objects.all()
    accounts = Account.objects.all()

    return render(request, 'adCampaigns/createAdCampaign.html', {
        'form': form,
        'contacts': contacts,
        'accounts': accounts,
    })



def adCampaign(request, id):
  campaign = get_object_or_404(AdvertisingCampaignSummary, id=id)
  return render(request, 'adCampaigns/singleAdCampaign.html', {
      'campaign': campaign
  })

# Ads

def allAds(request):
  return render(request, 'adCampaigns/allAds.html')

def singleAd(request, ad_id):
  return render(request, 'adCampaigns/singleAd.html')

def createAd(request):
  return render(request, 'adCampaigns/createAd.html')


# Advertisers Search
def advertiser_search(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        accounts = Account.objects.filter(
            Q(company_name_1__icontains=query) |
            Q(account_number__icontains=query) |
            Q(address__icontains=query) |
            Q(phone__icontains=query)
        )[:10]  # limit results

        results = [
            {
                'id': acc.id,
                'name': acc.company_name_1 or acc.account_number,
                'phone': acc.phone,
                'address': acc.address,
            }
            for acc in accounts
        ]

    return JsonResponse({'results': results})
