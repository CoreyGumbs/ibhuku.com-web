from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def ProfileLogin(request):
	return render(request, 'log/login.html')