from django.shortcuts import render

def index(request):
  return render(request, 'adCampaigns/allCampaigns.html')

def adCampaign(request):
  return render(request, 'adCampaigns/singleAdCampaign.html')

def createCampaign(request):
  return render(request, 'adCampaigns/createAdCampaign.html')
