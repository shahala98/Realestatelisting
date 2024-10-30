from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    id_proof = models.FileField(upload_to='id_proofs/', blank=True, null=True)
    saved_search = models.JSONField(blank=True, null=True)
    is_agent = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f'{self.user.username} Profile'

class Listing(models.Model):
    PROPERTY_TYPE = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Condo', 'Condo'),
    ]
    
    LISTING_TYPE = [
        ('Rent', 'Rent'),
        ('Sale', 'Sale'),
        ('Lease', 'Lease')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE, null=True)  
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    square_feet = models.IntegerField()
    image = models.ImageField(upload_to='listing/')
    listing_date = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
  
   

    def __str__(self):
        return self.title
    
class PropertyImage(models.Model):
    listing = models.ForeignKey('Listing', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing/images/')

    def __str__(self):
        return f"Image for {self.listing.title}"



class Property(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('hidden', 'Hidden'),
    ]
    
    PROPERTY_TYPE_CHOICES = [
        ('rent', 'Rent'),
        ('buy', 'Buy'),
    ]

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    property_type = models.CharField(max_length=4, choices=PROPERTY_TYPE_CHOICES, default='rent') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=1)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"Review for {self.listing.title} by {self.user.username} - Rating: {self.rating}"

class Favorite(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"{self.user.username} - {self.listing.title}"
    



