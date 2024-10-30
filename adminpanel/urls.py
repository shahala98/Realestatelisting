from django.urls import path
from.views import (admin_home,manage_list,toggle_property_status,user_list,list_reviews,agent_properties,
                   admin_profile,edit_profile,deactivate_property,activate_property,view_property,deactivate_review,
                   activate_review,user_detail_view)

app_name = 'adminpanel'

urlpatterns = [
    path('',admin_home,name='admin_home'),
    path('properties/', manage_list, name='manage_listing'),
    path('properties/toggle/<int:property_id>/', toggle_property_status, name='toggle_property_status'),
    path('userlist',user_list,name='user_list'),
    path('Review',list_reviews,name='manage_reviews'),
    path('profile/', admin_profile, name='admin_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'), 
    path('property/deactivate/<int:property_id>/', deactivate_property, name='property_deactivate'),
    path('property/activate/<int:property_id>/',activate_property, name='property_activate'),
    path('adminpanel/view_property/<int:property_id>/', view_property, name='view_property'),
    path('agent-properties/', agent_properties, name='agent_properties'),
    path('reviews/activate/<int:review_id>/', activate_review, name='activate_review'),
    path('reviews/deactivate/<int:review_id>/', deactivate_review, name='deactivate_review'),
    path('user/<int:pk>/', user_detail_view, name='user_details'),
    



]
