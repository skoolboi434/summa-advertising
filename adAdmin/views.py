from django.shortcuts import render, redirect
from .models import Role, Region, Status
from users.models import AdvertisingUser
from adCampaigns.models import Publication, AccountType
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.urls import reverse


def index(request):
  return render(request, 'admin/portal.html')

def adminGeneral(request):
  return render(request, 'admin/general.html')

def adminPubSetup(request):
  return render(request, 'admin/pubs/newPublication.html')

# Admin Account Routes
def adminAccounts(request):
    accountTypes = AccountType.objects.all().order_by('-id')  # Show newest first
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

    return render(request, 'admin/accounts.html', {
        'page_obj': page_obj,
        'roles': roles,
        'statuses': statuses
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