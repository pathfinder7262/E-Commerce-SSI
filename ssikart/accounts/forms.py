from attr import attributes
from django import forms
from accounts.models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"Enter Pass"
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"confirm Pass"
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

def __init__(self,*args,**kwargs):
    super(RegistrationForm,self).__init__(*args,**kwargs)
    self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
    self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
    self.fields['phone_number'].widget.attrs['placeholder'] = "Enter First Name"
    self.fields['email'].widget.attrs['placeholder'] = "Enter E-mail"

    for field in self.fields:
        self.fields[field].widget.attrs['class'] = "form-control"

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        pwd = cleaned_data.get("password")
        confirm_pwd = cleaned_data.get("confirm_password")

        if pwd != confirm_pwd:
            raise forms.validationError("Password Do Not Match..!")