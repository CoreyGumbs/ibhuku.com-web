from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

# Create your views here.


class profile_index(TemplateView):
	template_name = 'profiles/login_required.html'

@login_required
def ProfileDashboard(request, pk=None):
	return render(request, 'profiles/dashboard.html')

def ProfileLogin(request):
	return render(request, 'log/login.html')