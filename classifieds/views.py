from django.shortcuts import render
from .models import ClassifiedAd, Classification
from adAdmin.models import Publication, SalesPerson, Customer
from django.core.paginator import Paginator
from django.http import JsonResponse


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
  pub_list = Publication.objects.all()
  classification_list = Classification.objects.all()
  sales_person_list = SalesPerson.objects.all()
  customers = Customer.objects.all()
  return render(request, 'classifieds/createClassified.html', {
    'pub_list': pub_list,
    'classification_list': classification_list,
    'sales_person_list': sales_person_list,
    "customers": customers
  })

def search_customers(request):
    q = request.GET.get("q", "").strip()
    customers = Customer.objects.filter(
        models.Q(first_name__icontains=q) |
        models.Q(last_name__icontains=q) |
        models.Q(company_1__icontains=q) |
        models.Q(company_2__icontains=q)
    )[:20]

    return JsonResponse({
        "results": [
            {
                "id": c.id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "phone": c.phone,
            }
            for c in customers
        ]
    })