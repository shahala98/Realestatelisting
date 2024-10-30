
from django.shortcuts import get_object_or_404, redirect, render
from Agent.forms import ProfileForm
from adminpanel import models
from adminpanel.models import Listing,Favorite, Profile, Review
from users.forms import  ReviewForm, UserForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import logout



# Create your views here.

# def home(request):
#     # Fetch properties where the agent's profile exists and the status is 'active'
#     properties = Listing.objects.filter(
#         agent__isnull=False,
#         is_active=True
#     )
   
#     return render(request, 'users/users_home.html', {
#         'properties': properties,
        
#     })



def home(request):
    property_list = Listing.objects.filter(agent__isnull=False, is_active=True)

    # Create paginator for the properties list
    paginator = Paginator(property_list, 6)
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)

    # Fetch user's favorites
    user_favorites = Favorite.objects.filter(user=request.user).values_list('listing_id', flat=True) if request.user.is_authenticated else []

    # Annotate each property with is_favorited
    for property in properties:
        property.is_favorited = property.id in user_favorites

    return render(request, 'users/users_home.html', {
        'properties': properties,
        'paginator': paginator,
    })



def all_property(request):
    properties = Listing.objects.filter(agent__isnull=False, is_active=True)
    return render(request, 'users/propertys.html', {'properties': properties})

def rent_properties(request):
    properties = Listing.objects.filter(listing_type='Rent', is_active=True)  # Adjusted for 'Rent'
    return render(request, 'users/rent_propertys.html', {'properties': properties})

def buy_properties(request):
    properties = Listing.objects.filter(listing_type='Sale', is_active=True)  # Adjusted for 'Sale'
    return render(request, 'users/buy_propertys.html', {'properties': properties})


def lease_properties(request):
    properties = Listing.objects.filter(listing_type='Lease',is_active=True)  # Filter for lease properties
    return render(request, 'users/lease_propertys.html', {'properties': properties})





def view_property(request, property_id):
    # Fetch the property by its ID
    property = get_object_or_404(Listing, id=property_id)

    # Check if the property is already a favorite for the user
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, listing=property).exists()

    # Fetch related images and active reviews
    images = property.images.all()  # Assuming a related name for images exists
    reviews = property.reviews.filter(is_active=True)  # Only include active reviews

    # Handle form submission for adding a review
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to add a review.')
            return redirect('login')  # Redirect to login if the user is not authenticated

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = property  # Link review to the property
            review.user = request.user  # Link review to the current user
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('users:view_property', property_id=property.id)
        else:
            messages.error(request, 'There was an error adding your review. Please correct the errors below.')
    else:
        form = ReviewForm()  # Instantiate a new review form for GET requests

    # Pass the property, images, reviews, favorite status, and form to the template
    context = {
        'property': property,
        'images': images,
        'reviews': reviews,
        'is_favorite': is_favorite,
        'form': form,
    }
    return render(request, 'users/view_property.html', context)


def add_review(request, property_id):
    listing = get_object_or_404(Listing, id=property_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.user = request.user
            review.save()
            return redirect('view_property', property_id=property_id)
    return redirect('view_property', property_id=property_id)

def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Check if the user is the author of the review
    if review.user != request.user:
        messages.error(request, 'You do not have permission to edit this review.')
        return redirect('users:view_property', property_id=review.listing.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('users:view_property', property_id=review.listing.id)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'users/edit_review.html', context)

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Check if the user is the author of the review
    if review.user != request.user:
        messages.error(request, 'You do not have permission to delete this review.')
        return redirect('users:view_property', property_id=review.listing.id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted successfully!')
        return redirect('users:view_property', property_id=review.listing.id)

    return render(request, 'users/delete_review.html', {'review': review})


def add_to_favorites(request, property_id):
    property = get_object_or_404(Listing, id=property_id)
    
    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user, listing=property)
        if created:
            messages.success(request, f"{property.title} has been added to your favorites!")
        else:
            favorite.delete()  # Remove from favorites if it already exists
            messages.warning(request, f"{property.title} has been removed from your favorites!")
    else:
        messages.error(request, "You need to be logged in to manage favorites.")
    
    return redirect('users:view_property', property_id=property_id)


def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    return render(request, 'users/favorite.html', {'favorites': favorites})
  
def remove_favorite(request, listing_id):
    try:
        # Get the favorite entry for the current user and the specified listing
        favorite = get_object_or_404(Favorite, user=request.user, listing_id=listing_id)
        favorite.delete()  # Remove the favorite
        messages.success(request, 'Favorite property removed successfully.')
    except Exception as e:
        messages.error(request, 'An error occurred while trying to remove the favorite property.')

    return redirect('users:favorite') 




def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:user_profile')  
    else:
        user_form = ProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'users/user_profile.html', {
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
            return redirect('users:user_profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'profile': profile,
    }
    
    return render(request, 'users/edit_profile.html', context)


def delete_profile(request):
    # Ensure we get the correct profile for the logged-in user
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        if 'delete' in request.POST:
            user = request.user
            
            # Check if the profile belongs to a client
            if not profile.is_agent:  
                # Handle deletion for client profile
                profile.delete()  # Deletes the client profile
                user.delete()  # Delete the user account itself
                logout(request)  # Logs out the user
                messages.success(request, 'Client account and all associated data have been deleted.')
                return redirect('Homeapp:client_login')  # Redirect to the login page
            else:
                # Handle the case if the user tries to delete an agent profile with this view
                messages.error(request, 'You cannot delete an agent profile using this function.')
                return redirect('users:user_profile')  # Redirect to view profile for agents

        elif 'cancel' in request.POST:
            messages.info(request, 'Account deletion canceled.')
            return redirect('users:user_profile')  # Redirect to view profile

    return render(request, 'users/profile_delete.html', {'profile': profile})

def search_view(request):
    query = request.GET.get('query', '')
    property_type = request.GET.get('property_type', '')
    listing_type = request.GET.get('listing_type', '')

    # Base queryset for active listings
    results = Listing.objects.filter(is_active=True)

    print(f"Query: {query}, Property Type: {property_type}, Listing Type: {listing_type}")  # Debugging line

    # Filter by search query
    if query:
        results = results.filter(title__icontains=query)
        print(f"Results after query filter: {results.count()}")  # Debugging line

    # Filter by property type
    if property_type:
        results = results.filter(property_type=property_type)
        print(f"Results after property type filter: {results.count()}")  # Debugging line

    # Filter by listing type
    if listing_type:
        results = results.filter(listing_type=listing_type)
        print(f"Results after listing type filter: {results.count()}")  # Debugging line

    context = {
        'results': results,
        'query': query,
        'property_type': property_type,
        'listing_type': listing_type,
    }

    return render(request, 'users/search.html', context)



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)