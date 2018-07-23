from django.shortcuts import render,HttpResponse

# Create your views here.
def index(reuqest):

    return HttpResponse("this is user!")