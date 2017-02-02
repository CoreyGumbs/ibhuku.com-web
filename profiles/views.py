from django.shortcuts import render
from django.http import HttpResponse

from accounts.models import IbkUser, Profile

# Create your views here.
def ProfileDashboardView(request, name):
	usr_name = IbkUser.objects.get(name=name)
	return render(request, 'profiles/profile_dashboard.html')