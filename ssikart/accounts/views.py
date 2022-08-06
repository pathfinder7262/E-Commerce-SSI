from email import message

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from requests import post
from django.contrib.auth.tokens import default_token_generator

from accounts.forms import RegistrationForm
from accounts.models import Account

from carts.models import Cart, CartItem
from carts.utils import _cart_id

# Create your views here.

def register(request):
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phone_number = form.cleaned_data.get("phone_number")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name, last_name, username, email, password
            )
            user.phone_number = phone_number
            user.save()
            messages.success(request, "Registration Successful !")

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "SSI Ecommerce | Please Activate Account"
            message = render_to_string(     
                "accounts/account_varification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #print("email sent")
            # messages.success(request, 'Thank You for registering with us. We have sent you the verification email to your email address. Please verify if for login.')
            return redirect("/accounts/login/?command=verification&email=" + email)

            # return redirect("registration")
        form = RegistrationForm()

    context_data = {"form": form}
    return render(request, "accounts/register.html", context_data)




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your Account has been successfully activated!")
        return redirect("login")
    else:
        messages.error(request, "Invalid Activation Link")
        return redirect("registration")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(email=email, password=password)

        if user:
            try:
                print("Inside try")
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
                
            auth.login(request, user)
            #messages.success(request, "You are now logged in!")
            return redirect("ssi-main-home")
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect("login")

    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, 'You Logged Out Successfully..!')
    return redirect("login")

@login_required(login_url="login")
def dashboard(request):
    return render(request, "accounts/dashboard.html")


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # RESET PASSWORD SEND
            current_site = get_current_site(request)
            mail_subject = 'SSI Shop | Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email= EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email is sent to you email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.success(request, 'This link is expired!!!!')
        return redirect('login')

