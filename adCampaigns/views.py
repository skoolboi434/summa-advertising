from django.shortcuts import render, redirect, get_object_or_404
from .models import AdvertisingCampaignSummary, SalesPerson


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



