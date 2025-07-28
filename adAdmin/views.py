from django.shortcuts import render, redirect
from .models import Role, Region
from adCampaigns.models import Publication, AccountType
from django.core.paginator import Paginator

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

    if request.method == 'POST':
        print("📨 POST request received")
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()

        print(f"📥 Form values - name: '{name}', code: '{code}'")

        if name and code:
            new_type = AccountType.objects.create(name=name, code=code)
            print("✅ Created new AccountType:", new_type.id, new_type.name)
            return redirect('adminAccounts')
        else:
            print("⚠️ Name or code missing. Not creating.")

    return render(request, 'admin/accounts.html', {
        'page_obj': page_obj,
        'roles': roles,
    })



def createUser(request):
  roles = Role.objects.all()
  regions = Region.objects.all()
  publications = Publication.objects.all()
  
  return render(request, 'users/createUser.html', {
      'roles': roles,
      'regions': regions,
      'publications': publications,
      'accountTypes': accountTypes
  })

  return render(request, 'users/createUser.html')

# def createAccountType(request):
#     if request.method == 'POST':
#         name = request.POST.get('name', '').strip()
#         code = request.POST.get('code', '').strip()

#         if name and code:
#             AccountType.objects.create(name=name, code=code)
#             # You can redirect or add a success message here
#             return redirect('adminAccounts')  # or reload the same page

#     return render(request, 'admin/accounts.html')