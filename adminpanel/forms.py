from django import forms
from django.contrib.auth.models import User
from adminpanel.models import Listing,Review,Profile

class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )

class ListingAdminForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'location', 'property_type', 'bedrooms', 'bathrooms', 'square_feet', 'image', 'agent',  'is_active']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['listing', 'rating', 'comment']
        widgets = {
            'listing': forms.HiddenInput(),
            'rating': forms.Select(attrs={'class': 'form-control'}),  
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }       


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'phone', 'profile_image', 'id_proof']