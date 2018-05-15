from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User


def index(request):
    return render(request, "loginregistration_app/index.html")

def register(request):
    user = User.objects.validate_registration(request.POST)
    if user["status"]:
        request.session["first_name"] = user["obj"].first_name
        request.session["email"] = user["obj"].email
        request.session["status"] = "registered"
        return redirect("/success")
    else:
        for value in user["obj"].values():
            messages.error(request, value)
        return redirect("/")

def login(request):
    user = User.objects.validate_login(request.POST)
    if user["status"]:
        #print("login views:",user["obj"].first_name)
        #print(user["obj"].first_name)
        request.session["first_name"] = user["obj"].first_name
        request.session["email"] = user["obj"].email
        request.session["status"] = "logged in"
        return redirect("/success")
    else:
        for value in user["obj"].values():
            messages.error(request, value)
        return redirect("/")

def success(request):
    if "email" not in request.session:
        messages.error(request, "You must be logged in to access this page")
        return redirect("/")
    return render(request, "loginregistration_app/success.html")

def logout(request):
    request.session.clear()
    return redirect("/")
