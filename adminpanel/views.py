
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from adminpanel.forms import  ProfileForm, ReviewForm
from .models import Listing, Review,Profile
from django.contrib.auth.models import User

# Create your views here.

def admin_home(request):
    return render(request, 'adminpanel/admin_home.html' )


def manage_list(request):
    properties = Listing.objects.all() 
    return render(request, 'adminpanel/manage_listing.html', {'properties': properties})


def deactivate_property(request, property_id):
    property = get_object_or_404(Listing, id=property_id)
    try:
        property.is_active = False  
        property.save()
        messages.success(request, f'{property.title} has been deactivated.')
    except Exception as e:
        messages.error(request, f'Error deactivating {property.title}: {e}')
    
    return redirect('adminpanel:manage_listing')

def activate_property(request, property_id):
    property = get_object_or_404(Listing, id=property_id)
    try:
        property.is_active = True  
        property.save()
        messages.success(request, f'{property.title} has been activated.')
    except Exception as e:
        messages.error(request, f'Error activating {property.title}: {e}')
    
    return redirect('adminpanel:manage_listing')

    
def view_property(request, property_id):
    # Fetch the property by its ID
    property = get_object_or_404(Listing, id=property_id)
    
    # Fetch related images for the property
    images = property.images.all()  # Assuming you have a related name for images

    # Render the template with the property and its images
    return render(request, 'adminpanel/view_property.html', {'property': property, 'images': images})


def toggle_property_status(request, property_id):
    property_obj = get_object_or_404(Listing, id=property_id)
    property_obj.is_active = not property_obj.is_active
    property_obj.save()
    return redirect('adminpanel:manage_list')


def user_list(request):
    # Fetch only profiles where the user is a staff or superuser
    profiles = Profile.objects.filter(user__is_staff=False) | Profile.objects.filter(user__is_superuser=False)

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')

        profile = get_object_or_404(Profile, id=profile_id)
        user = profile.user

        try:
            if action == 'activate':
                profile.is_active = True
                user.is_active = True  # Activate the user
                messages.success(request, f'Profile {profile.user.username} activated.')
            elif action == 'deactivate':
                profile.is_active = False
                user.is_active = False  # Deactivate the user
                messages.success(request, f'Profile {profile.user.username} deactivated.')

            # Save both profile and user status
            profile.save()
            user.save()

        except Exception as e:
            messages.error(request, f'An error occurred while processing {profile.user.username}: {str(e)}')

        return redirect('adminpanel:user_list')  # Redirect to the same view after processing

    return render(request, 'adminpanel/user_list.html', {
        'profiles': profiles,
    })


def user_detail_view(request, pk):
    """Fetch a specific user and their profile details."""
    user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'adminpanel/user_details.html', {'user': user, 'profile': profile})


def list_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'adminpanel/manage_reviews.html', {'reviews': reviews})



def activate_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    try:
        review.is_active = True
        review.save()
        messages.success(request, 'Review activated successfully!')
    except Exception as e:
        messages.error(request, f'Error activating review: {e}')
    
    return redirect('adminpanel:manage_reviews')

def deactivate_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    try:
        review.is_active = False
        review.save()
        messages.success(request, 'Review deactivated successfully!')
    except Exception as e:
        messages.error(request, f'Error deactivating review: {e}')
    
    return redirect('adminpanel:manage_reviews')


def admin_profile(request):
    user = request.user

    # Try to get the profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('adminpanel:admin_profile')  
    else:
        
        user_form = ProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'adminpanel/admin_profile.html', {
        'profile_form': profile_form,
        'user_form': user_form,
        'user': user,
        'profile': profile,
    })


def edit_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('adminpanel:admin_profile')  # Redirect after successful update
        else:
            # Log or print out form errors for debugging
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = ProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'profile': profile,
        'messages': messages.get_messages(request),
    }
    return render(request, 'adminpanel/edit_profile.html', context)

def agent_properties(request):
    # Fetch all profiles where the user is an agent
    agents = Profile.objects.filter(is_agent=True)

    # Create a dictionary to hold agent profiles and their properties
    agent_data = {}
    
    for agent in agents:
        # Fetch properties related to this agent
        properties = Listing.objects.filter(agent=agent)  # Assuming Listing has a ForeignKey to Profile
        agent_data[agent] = properties  # Store agent and their properties

    return render(request, 'adminpanel/agent_properties.html', {
        'agent_data': agent_data,
    })