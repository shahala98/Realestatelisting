
from django import forms
from adminpanel.models import Profile,Listing
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'profile_picture']

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Agent Name"
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label="Agent Bio"
    )
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Profile Picture"
    )





# class PropertyForm(forms.ModelForm):
#     property_title = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         label="Property Title"
#     )
#     location = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         label="Location"
#     )
#     price = forms.DecimalField(
#         widget=forms.NumberInput(attrs={'class': 'form-control'}),
#         label="Price",
#         min_value=0.01  
#     )
#     property_type = forms.ChoiceField(
#         choices=Listing.PROPERTY_TYPE,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Property Type"
#     )
#     listing_type = forms.ChoiceField(
#         choices=Listing.LISTING_TYPE,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Listing Type"
#     )
#     bedrooms = forms.ChoiceField(
#         choices=[(i, f"{i} Bed{'s' if i > 1 else ''}") for i in range(1, 5)],
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Number of Bedrooms"
#     )
#     bathrooms = forms.ChoiceField(
#         choices=[(i, f"{i} Bath{'s' if i > 1 else ''}") for i in range(1, 5)],
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Number of Bathrooms"
#     )
#     square_feet = forms.IntegerField(
#         widget=forms.NumberInput(attrs={'class': 'form-control'}),
#         label="Square Feet"
#     )
#     property_description = forms.CharField(
#         widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the property...', 'rows': 4}),
#         label="Property Description",
#         help_text="Provide a detailed description of the property."
#     )
#     active = forms.BooleanField(
#         required=False,
#         initial=True,  
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         label="Is Active"
#     )
#     main_image = forms.ImageField(
#         widget=forms.FileInput(attrs={'class': 'form-control'}),
#         label="Image"
#     )

#     class Meta:
#         model = Listing
#         fields = [
#             'property_title', 'location', 'price', 'property_type',
#             'listing_type', 'bedrooms', 'bathrooms', 'square_feet',
#             'property_description', 'active', 'main_image', 'Profile'
#         ]


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude =['agent','favorited_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Include the 'title' field
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),  # For choice fields
            'listing_type': forms.Select(attrs={'class': 'form-control'}),  # For choice fields
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'square_feet': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }



# class PropertyForm(forms.ModelForm):
#     class Meta:
#         model = Listing
        
#         exclude = ['agent']
        
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

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']