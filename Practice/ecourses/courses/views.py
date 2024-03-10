from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    # e-courses app là view trả ra cho user
    return render(request, 'index.html')