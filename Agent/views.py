
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from Agent.forms import  ProfileForm, ProfilePhotoForm, PropertyForm,UserForm
from adminpanel.models import  Listing, Profile, PropertyImage, Review
from django.contrib.auth.models import User



# Create your views here.

def agent_home(request):
   
    return render(request, 'Agent/agent_home.html') 



def add_property(request):
    logged_user = request.user
    agent_profile = get_object_or_404(Profile, user=logged_user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.agent = agent_profile
            listing.save()
            
            # Save multiple images
            images = request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(listing=listing, image=image)

            # Add success message
            messages.success(request, 'Property added successfully!')
            return redirect('Agent:property_listing')
        else:
            # Add error message if form is invalid
            messages.error(request, 'Please correct the errors below.')
            # Instead of redirecting, render the form again
            return render(request, 'Agent/add_propertys.html', {'form': form})
    else:
        form = PropertyForm()

    return render(request, 'Agent/add_propertys.html', {'form': form})


def property_list(request):
    # Get the logged-in user's profile (assuming user is logged in and has a related profile)
    agent_profile = get_object_or_404(Profile, user=request.user)
    properties = Listing.objects.filter(agent=agent_profile, is_active=True)
    return render(request, 'Agent/property_listing.html', {'properties': properties})



def view_property(request):
    property_type = request.GET.get('type', 'all')
    # Get the logged-in user's profile (assuming user is logged in and has a related profile)
    agent_profile = get_object_or_404(Profile, user=request.user)
    # Filter the properties based on the logged-in agent
    if property_type == 'all':
        properties = Listing.objects.filter(agent=agent_profile, is_active=True)
    else:
        properties = Listing.objects.filter(agent=agent_profile, is_active=True, listing_type=property_type)
    return render(request, 'Agent/view_property.html', {
        'properties': properties, 
        'selected_type': property_type
    })



def property_details(request, property_id):
    # Fetch the property by its ID
    listing = get_object_or_404(Listing, id=property_id)
    
    # Restrict access if the logged-in user is not the property's agent
    if request.user != listing.agent.user:
        return HttpResponseForbidden("You are not allowed to view this property.")
    
    # Fetch related images and active reviews
    images = listing.images.all()  # Assuming related_name="images" in PropertyImage model
    reviews = listing.reviews.filter(is_active=True)  # Only active reviews
    
    # Render the template with the listing details, images, and reviews
    return render(request, 'Agent/property_details.html', {
        'property': listing,
        'images': images,
        'reviews': reviews
    })


def toggle_review_status(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Toggle the review status
    review.is_active = not review.is_active
    review.save()

    # Provide feedback to the user
    action = 'activated' if review.is_active else 'deactivated'
    messages.success(request, f'Review has been {action} successfully.')

    # Use the correct attribute to get the property
    return redirect('Agent:property_details', property_id=review.property.id)  # Make sure 'property' exists in Review






def edit_property(request, property_id):
    property = get_object_or_404(Listing, id=property_id)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            property = form.save()  # Save the property instance

            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(listing=property, image=image)

            messages.success(request, 'Property updated successfully!')
            return redirect('Agent:property_details', property_id=property.id)
    else:
        form = PropertyForm(instance=property)

    return render(request, 'Agent/edit_property.html', {'form': form, 'property': property})


def delete_property(request, property_id):
    listing = get_object_or_404(Listing, id=property_id)
    listing.delete()
    messages.success(request, 'Property deleted successfully.')
    return redirect('Agent:property_listing')


def agent_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('Agent:agent_profile')  
    else:
        user_form = ProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'Agent/agent_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'profile': profile,
    })


def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  # Ensure profile exists

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('Agent:agent_profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'profile': profile,
    }
    
    return render(request, 'Agent/profile_info.html', context)

def delete_profile(request):
    # Get the user's profile linked to the logged-in user
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Check if the user has confirmed the deletion
        if 'delete' in request.POST:
            user = request.user
            
            # Check if the profile is an agent's profile
            if profile.is_agent:
                # Optionally handle agent-specific cleanup here if needed
                pass
            
            try:
                # Delete the profile
                profile.delete()
                # Delete the user account
                user.delete()
                # Logout the user
                logout(request)
                
                messages.success(request, 'Your account and all associated data have been deleted.')
                return redirect('Homeapp:agent_login')  # Redirect to the login page

            except Exception as e:
                messages.error(request, f'Error deleting profile: {e}')
                return redirect('Agent:agent_profile')  # Redirect to view profile on error

        elif 'cancel' in request.POST:
            messages.info(request, 'Account deletion canceled.')
            return redirect('Agent:agent_profile')  # Redirect to view profile

    return render(request, 'Agent/account_delete.html', {'profile': profile})



def user_logout(request):
    logout(request)
    return redirect('Homeapp:home')

def settings_view(request):
    
    return render(request, 'Agent/settings.html')

