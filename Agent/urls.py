from django.urls import path
from .views import (agent_home,add_property, delete_property, edit_property, property_list,view_property,toggle_review_status,
                    agent_profile,user_logout,settings_view,edit_profile,property_details,delete_profile,
                    
                    )

app_name = 'Agent'
urlpatterns = [
    path('',agent_home,name='agent_home'),
    path('add-property/', add_property, name='add_propertys'),
    path('property_listing/', property_list, name='property_listing'),
    path('view_properties/', view_property, name='view_property'), 
    path('property/edit/<int:property_id>/', edit_property, name='edit_property'),
    path('Agent/delete/<int:property_id>/', delete_property, name='delete_property'),
    path('user_logout/', user_logout, name='user_logout'),
    path('settings/',settings_view, name='settings'),
    path('profile_info/',edit_profile, name='profile_info'),
    path('profile/', agent_profile, name='agent_profile'),
    path('Agent/property_details/<int:property_id>/', property_details, name='property_details'),
    path('Agent/edit_property/<int:property_id>/', edit_property, name='edit_property'),
    path('delete_account/',delete_profile,name='account_delete'),
    path('toggle_review_status/<int:review_id>/', toggle_review_status, name='toggle_review_status'),
]
