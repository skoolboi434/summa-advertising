from django.shortcuts import render


def index(request):
  return render(request, 'users/allUsers.html')

def userProfile(request, user_id):
  return render(request, 'users/userProfile.html')
