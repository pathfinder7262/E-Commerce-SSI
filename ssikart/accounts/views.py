from django.shortcuts import render
from accounts.forms import Registrationform
from accounts.models import Account
# Create your views here.
def register(request):
    form = Registrationform()
    context_data = {
        'form' : form
    }
    return render(request,"accounts/register.html", context_data)

def login(request):
    return render(request,"accounts/login.html")


def logout(request):
    return render(request,"accounts/logout.html")   