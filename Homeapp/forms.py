from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from adminpanel.models import Profile
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Username"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email"
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="First Name"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Last Name"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password and confirm_password and password != confirm_password:
            self.add_error('password2', "Passwords do not match")

        return cleaned_data

    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'about', 'profile_image', 'id_proof']

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']
    
# Creating a User Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'form3Example3',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'form3Example4',
        'placeholder': 'Password'
    }))
   
# class LoginForm(AuthenticationForm):
#     user_type = forms.ChoiceField(choices=[
#         ('user', 'User'),
#         ('agent', 'Agent')
#     ])
#     email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={
#         'class': 'form-control',
#         'id': 'form3Example3',
#         'placeholder': 'Email address'
#     }))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'id': 'form3Example4',
#         'placeholder': 'Password'
#     }))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email Address', max_length=254)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is not registered.")
        return email

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        label='OTP',
        max_length=6,
        widget=forms.HiddenInput()  # Keep the main field hidden; OTP will be submitted from individual inputs
    )

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data