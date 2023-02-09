from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}), error_messages={'unique':"A user with this username already exists."}, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), required=True)

    class Meta:
        model=User
        fields=['username', 'password']

    def clean(self):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        cleaned_data=super(RegisterUserForm, self).clean()
        password=cleaned_data.get("password")
        username =cleaned_data.get('username')

        if len(username) < 8:
            self.add_error('username','Username length must be greater than 8 character.')
        if not any (char in special_characters for char in password):
            self.add_error('password','Password must contain at least one special Character.')

        if len(password)  < 8:
            self.add_error('password','Password length must be greater than 8 character.')
        if not any (char.isdigit() for char in password):
            self.add_error('password','Password must contain at least one digit.')
        if not any (char in special_characters for char in password):
            self.add_error('password','Password must contain at least one special Character.')

        return cleaned_data

class RegisterExtraForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email ID'}), error_messages={'unique':"This email has already been registered."}, required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mobile Number'}), error_messages={'unique':"This Mobile number has already been registered."}, required=True)

    class Meta:
        model=Register
        fields=['email', 'name', 'phone']

#<-----Visistor Login Form----->#
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), required=True)

class ForgotpassForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email ID'}), required=True)

class ContactusForm(forms.ModelForm):
    class Meta:  
        model = Contact 
        fields = "__all__"  

class InvestorsForm(forms.ModelForm): 
    class Meta:  
        model = Investor 
        fields = "__all__" 

class InstructorForm(forms.ModelForm):  
    class Meta:  
        model = Instructor  
        fields = "__all__"  

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Old Password'}), required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New Password'}), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm New Password'}), required=True)
