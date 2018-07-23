from django.shortcuts import render,HttpResponse,reverse

# Create your views here.

def index(request):

    return HttpResponse(reverse('index'))