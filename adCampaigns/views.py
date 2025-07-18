from django.shortcuts import render, redirect, get_object_or_404



# Ad Campaigns 
def index(request):
  return render(request, 'adCampaigns/allCampaigns.html')

def createCampaign(request):
  return render(request, 'adCampaigns/createAdCampaign.html')

def adCampaign(request, campaign_id):
    return render(request, 'adCampaigns/singleAdCampaign.html')

# Ads

def allAds(request):
  return render(request, 'adCampaigns/allAds.html')

def singleAd(request, ad_id):
  return render(request, 'adCampaigns/singleAd.html')

def createAd(request):
  return render(request, 'adCampaigns/createAd.html')



