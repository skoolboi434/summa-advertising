from django.shortcuts import render, redirect, get_object_or_404
from adCampaigns.models import Account
from django.core.paginator import Paginator

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
  return render(request, 'advertisers/singleAdvertiser.html', {
    'advertiser': advertiser
  })

def createAdvertiser(request):
  return render(request, 'advertisers/createAdvertiser.html')