from django.urls import path
from .views import (home,all_property,rent_properties,favorites_view,buy_properties,
                  view_property,add_review,profile_view,search_view,edit_review,delete_review
                    ,lease_properties,add_to_favorites,edit_profile,remove_favorite,delete_profile,custom_404_view)

app_name = 'users'
urlpatterns = [
    path('',home,name='users_home'),
    path('property/',all_property,name='propertys'),
    path('rent_propertys/',rent_properties,name='rent_propertys'),
    path('buy/', buy_properties, name='buy_propertys'),
    path('users/property/<int:property_id>/',view_property,name='view_property'),
    path('users/property/<int:property_id>/review/', add_review, name='review'),
    path('profile/', profile_view, name='user_profile'),
    path('search/', search_view, name='search'),
    path('lease-properties/', lease_properties, name='lease_propertys'),
    path('edit_profile/', edit_profile, name='edit_profile'), 
    path('review/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),
    path('property/<int:property_id>/add-to-favorites/', add_to_favorites, name='add_to_favorites'),
    path('favorites/', favorites_view, name='favorite'),
    path('remove_favorite/<int:listing_id>/', remove_favorite, name='remove_favorite'),
    path('delete_profile/', delete_profile, name='profile_delete'),
    path('404/',custom_404_view,name='404')


    



]
