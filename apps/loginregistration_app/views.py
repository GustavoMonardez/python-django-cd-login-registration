from django.shortcuts import render, HttpResponse, redirect

def index(request):
    return render(request, "loginregistration_app/index.html")
