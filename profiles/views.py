from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def ProfileDashboardView(request):
	return render(request, 'profiles/profile_dashboard.html')