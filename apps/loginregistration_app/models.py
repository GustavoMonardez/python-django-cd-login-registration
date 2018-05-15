from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def validate_registration(self,data):
        errors = {}
        # first name validation
        if len(data["first_name"]) < 2:
            errors["first_name"] = "First name must contain at least 2 characters (letters only)"
        elif not data["first_name"].isalpha():
            errors["first_name"] = "First name must only contain letters"
        # last name validation
        if len(data["last_name"]) < 2:
            errors["last_name"] = "Last name must contain at least 2 characters (letters only)"
        elif not data["last_name"].isalpha():
            errors["last_name"] = "Last name must only contain letters"
        # check if account already registered        
        if len(User.objects.filter(email = data["email"])) > 0:
            errors["email"] = "An account already exists with that email"
        # email validation
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(data["email"]):
            errors["email"] ="Invalid Email Address!"
        # password validation
        if data["password"] != data["cpassword"]:
            errors["password"] = "Password and confirm password must match"
        elif len(data["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters long"
        # return either a user or an error
        if not errors:
            password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=data["first_name"],last_name=data["last_name"],email=data["email"],password=password)
            context = {"obj":user,"status":True}
            return context
        else:
            context = {"obj":errors,"status":False}
            return context
    
    def validate_login(self,data):
        errors = {}
        user = User.objects.filter(email=data["email"])
        if not user or not bcrypt.checkpw(data["password"].encode(), user[0].password.encode()) or not User.objects.filter(email = data["email"]):
            errors["login"] = "Could not log in"
        if not errors:
            context = {"obj":user[0],"status":True}
            return context
        else:
            context = {"obj":errors,"status":False}
            return context

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
