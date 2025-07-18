from django.shortcuts import render

def index(request):
  return render(request, 'admin/portal.html')

def adminGeneral(request):
  return render(request, 'admin/general.html')

def adminPubSetup(request):
  return render(request, 'admin/pubs/newPublication.html')