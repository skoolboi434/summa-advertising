from django.shortcuts import render, redirect
from .models import Role, Region, Status, AccountType, Publication
from classifieds.models import Classification
from users.models import AdvertisingUser
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def index(request):
  return render(request, 'admin/portal.html')

def adminGeneral(request):
  return render(request, 'admin/general.html')

def adminPubSetup(request):
  return render(request, 'admin/pubs/newPublication.html')

def adminAds(request):
  return render(request, 'admin/ads.html')

# Admin Account Routes

def adminAccounts(request):
    accountTypes = AccountType.objects.all().order_by('-id')
    users = AdvertisingUser.objects.all().order_by('-id')
    roles = Role.objects.all().order_by('-id')
    paginator = Paginator(accountTypes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    statuses = Status.objects.all()
    if request.method == 'POST':
        print("📨 POST request received")
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()
        status_id = request.POST.get('status')

        print(f"📥 Form values - name: '{name}', code: '{code}', status: '{status_id}'")

        status_obj = Status.objects.filter(id=status_id).first()

        if name and code and status_id:
            status_obj = Status.objects.filter(id=status_id).first()
            new_type = AccountType.objects.create(name=name, code=code, status=status_obj)
            print("✅ Created new AccountType:", new_type.id, new_type.name)
            return redirect('adminAccounts')
        else:
            print("⚠️ Name or code missing. Not creating.")
    
    can_edit_account_type = request.user.has_perm('adAdmin.change_accounttype')
    can_delete_account_type = request.user.has_perm('adAdmin.delete_accounttype')

    return render(request, 'admin/accounts.html', {
        'page_obj': page_obj,
        'roles': roles,
        'statuses': statuses,
        'users': users,
        'can_edit_account_type': can_edit_account_type,
        'can_delete_account_type': can_delete_account_type,
    })

def createUser(request):
    roles = Role.objects.all()
    regions = Region.objects.all()
    publications = Publication.objects.all()
    accountTypes = AccountType.objects.all().order_by('-id')
    statuses = Status.objects.all().order_by('name')

    if request.method == 'POST':
        data = request.POST

        user = AdvertisingUser.objects.create(
            first_name=data.get('first_name', '').strip(),
            last_name=data.get('last_name', '').strip(),
            username=data.get('username', '').strip(),
            nickname=data.get('nickname', '').strip() or None,
            email=data.get('email', '').strip(),
            phone=data.get('phone', '').strip() or None,
            website=data.get('website', '').strip() or None,
            bio=data.get('bio', '').strip() or None,
            language=data.get('language', '').strip() or None,
            status_id=data.get('status') or None,
            region_id=data.get('region') or None,
            role_id=data.get('role') or None,
            commission=data.get('commission') or 0.0,
            created_at=now(),
            updated_at=now(),
        )
        return redirect(reverse('userProfile', kwargs={'id': user.id}))

    return render(request, 'users/createUser.html', {
        'statuses': statuses,
        'roles': roles,
        'regions': regions,
        'publications': publications,
        'accountTypes': accountTypes
    })

def adminClassifieds(request):
    classification_list = Classification.objects.all()
    category_paginator = Paginator(classification_list, 15)

    page_number = request.GET.get('page')
    page_obj = category_paginator.get_page(page_number)

    return render(request, 'admin/classifieds.html', {'page_obj': page_obj})

def createAdminStyle(request):

    return render(request, 'admin/includes/classifieds/createAdminStyle.html')