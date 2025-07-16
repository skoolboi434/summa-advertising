from django.shortcuts import render

def index(request):
  return render(request, 'advertisers/allAdvertisers.html')

def advertiser(request, advertiser_id):
  return render(request, 'advertisers/singleAdvertiser.html')

def createAdvertiser(request):
  return render(request, 'advertisers/createAdvertiser.html')