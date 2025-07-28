from django.shortcuts import render, get_object_or_404
from users.models import AdvertisingUser
from adAdmin.models import Region, Role 


def index(request):
  return render(request, 'users/allUsers.html')

def userProfile(request, id):
  user = get_object_or_404(AdvertisingUser, id=id)
  roles = Role.objects.all()
  regions = Region.objects.all()
  return render(request, 'users/userProfile.html', {
      'user': user,
      'roles': roles,
      'regions': regions,
  })
