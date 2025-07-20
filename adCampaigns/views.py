from django.shortcuts import render, redirect, get_object_or_404
from .models import AdvertisingCampaignSummary, SalesPerson, Account
from django.db.models import Q
from django.http import JsonResponse

def index(request):
    campaigns = AdvertisingCampaignSummary.objects.all()
    return render(request, 'adCampaigns/allCampaigns.html', {
        'campaigns': campaigns
    })

def createCampaign(request):
  contacts = SalesPerson.objects.all()
  return render(request, 'adCampaigns/createAdCampaign.html', {'contacts': contacts})

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
