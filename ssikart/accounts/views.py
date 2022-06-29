from email import message
from django.shortcuts import render,redirect
from requests import post
from accounts.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from django.contrib import messages,auth

# Create your views here.
def register(request):
    form = RegistrationForm()

    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name =  form.cleaned_data.get("last_name")
            phone_number = form.cleaned_data.get("phone_number")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name, last_name, username, email, password )
            user.phone_number = phone_number
            user.save() 
            messages.success(request,'Registration successful....!') 
            return redirect('registration')
            form = RegistrationForm()

    context_data = {
        'form' : form
    }
    return render(request,"accounts/register.html", context_data)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(email=email, password=password)

        if user:
            auth.login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("ssi-main-home")
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect("login")

    return render(request, "accounts/login.html")

def dashboard(request):
    return render(request, "accounts/dashboard.html")

@login_required(login_url = "login")
def logout(request):
    auth.logout(request)
    messages.success(request,'You Logged Out Successfully..!')
    return render(request,"accounts/logout.html")   

