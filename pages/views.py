from django.shortcuts import render
from django.http import HttpResponse
from adCampaigns.models import AdvertisingCampaignSummary
from django.core.paginator import Paginator

def index(request):
  campaigns = AdvertisingCampaignSummary.objects.all()
  paginator = Paginator(campaigns, 10) 
  
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'pages/index.html', {
        'page_obj': page_obj
    })