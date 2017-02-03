from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from accounts.models import IbkUser, Profile

# Create your views here.
@login_required
def ProfileDashboardView(request, name=None):
	usr_name = IbkUser.objects.get(name=name)
	return render(request, 'profiles/profile_dashboard.html')