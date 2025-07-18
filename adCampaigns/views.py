from django.shortcuts import render

def index(request):
  return render(request, 'adCampaigns/allCampaigns.html')

def adCampaign(request, campaign_id):
  return render(request, 'adCampaigns/singleAdCampaign.html')

def createCampaign(request):
  return render(request, 'adCampaigns/createAdCampaign.html')

def createAd(request):
  return render(request, 'adCampaigns/createAd.html')

# Ads

def allAds(request):
  return render(request, 'adCampaigns/allAds.html')

def singleAd(request, ad_id):
  return render(request, 'adCampaigns/singleAd.html')
