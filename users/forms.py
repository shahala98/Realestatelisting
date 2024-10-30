from django import forms
from adminpanel.models import Listing, Profile, Review,  Favorite
from django.contrib.auth.models import User

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'location', 'property_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['listing']  # Exclude 'listing' field from the form
        fields = ['rating', 'comment']  # Specify the fields to include in the form
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control', 
                'aria-label': 'Rating'  # Add ARIA label for accessibility
            }),  
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,  # Specify the number of rows for better visibility
                'placeholder': 'Write your review here...'  # Placeholder text for guidance
            }),
        }

        
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
    property_type = forms.ChoiceField(
        choices=[
            ('', 'All'),  # Option to search all types
            ('rent', 'Rent'),
            ('sale', 'Sale'),
            ('lease', 'Lease'),
            ('house', 'House'),
            ('apartment', 'Apartment'),
            ('condo', 'Condo'),
            ('land', 'Land'),
        ],
        required=False,
    )



class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['listing', 'user']
        widgets = {
            'listing': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }




class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'about', 'profile_image', 'id_proof']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_proof': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }