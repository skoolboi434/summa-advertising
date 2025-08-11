from django.shortcuts import render
from .models import ClassifiedAd, Classification
from django.core.paginator import Paginator


def index(request):
  classified_list = ClassifiedAd.objects.all().order_by('-date_created')
  paginator = Paginator(classified_list, 15)
  #ClassifiedAd.classification = Classification.objects.first()
  # for ad in classified_list:
  #   print(f"First Name for ad {ad.id}: {ad.firstName}")

  
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, 'classifieds/allClassifieds.html', {
      'page_obj': page_obj
  })


def createClassified(request):

  return render(request, 'classifieds/createClassified.html')