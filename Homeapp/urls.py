from django.urls import path
from.views import (home_view,registration_view,login_view,agent_registration,agent_login,reset_password,
forgot_password,otp,about,contact,admin_login,property,services)


app_name = 'Homeapp'
urlpatterns = [
    path('',home_view,name='home'),
    path('registration/',registration_view, name='client_registration'),
    path('login/',login_view, name='client_login'),
    path('agent_registration/',agent_registration,name='agent_registration'),
    path('agent_login/',agent_login,name='agent_login'),
    path('reset_password/',reset_password,name='reset_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp-reset/', otp, name='otp'),
    path('about/',about,name="about"),
    path('contact/',contact,name='contact'),
    path('admin_login/',admin_login,name='admin_login'),
    path('property/',property,name='property'),
    path('service/',services,name='services'),
   
    
    
    



]