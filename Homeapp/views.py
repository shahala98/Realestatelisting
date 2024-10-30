
import random
from django.conf import settings
from django.contrib import messages
from django.template import RequestContext
from adminpanel.models import Profile 
from .forms import  OTPVerificationForm, RegistrationForm,LoginForm
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template 
from django.core.mail import send_mail
from django.shortcuts import  render,redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def home_view(request):
    return render(request,'Homeapp/home.html')

# def registration_view(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False) 
#             user.set_password(form.cleaned_data['password1'])
#             user.save()         
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
     
#             htmly = get_template('Homeapp/welcome_email.html')
#             context = {'username': username}  
#             subject = 'Welcome to Our Platform!'
#             from_email = 'your_email@gmail.com'
#             to = email

#             html_content = htmly.render(context)
#             msg = EmailMultiAlternatives(subject, '', from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()

#             messages.success(request, "Successfully Registered! Now you can log in.")
#             return redirect('Homeapp:client_login')  

#         else:
          
#             messages.error(request, "Registration failed. Please check the details and try again.")
#     else:
#         form = RegistrationForm() 

#     return render(request, 'Homeapp/client_registration.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # Log cleaned data for debugging
#             print(form.cleaned_data)

#             # Authenticate using the username and password
#             auth_user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
#             if auth_user is not None:
#                 login(request, auth_user) 
#                 messages.success(request, "Successfully logged in. Welcome to the Home Page!") 
#                 return redirect('users:users_home')  
#             else:
#                 messages.error(request, "Login failed. Please check your username and password again.")
#     else:
#         form = LoginForm()

#     return render(request, 'Homeapp/client_login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Create profile and set is_agent to False for clients
            Profile.objects.create(user=user, is_agent=False)

            # # Send welcome email
            # username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            # htmly = get_template('Homeapp/welcome_email.html')
            # context = {'username': username}
            # subject = 'Welcome to Our Platform!'
            # from_email = 'your_email@gmail.com'
            # to = email

            # html_content = htmly.render(context)
            # msg = EmailMultiAlternatives(subject, '', from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            messages.success(request, "Successfully Registered! Now you can log in.")
            return redirect('Homeapp:client_login')
        else:
            messages.error(request, "Registration failed. Please check the details and try again.")
            return redirect('Homeapp:client_registration')
    else:
        form = RegistrationForm()

    return render(request, 'Homeapp/client_registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if auth_user is not None:
                profile = Profile.objects.get(user=auth_user)
                
                if not profile.is_agent: 
                    login(request, auth_user)
                    messages.success(request, "Successfully logged in. Welcome to the Home Page!")
                    return redirect('users:users_home')
                else:
                    messages.error(request, "Only clients are allowed to log in here.")
                    return redirect('Homeapp:client_login')
                    
            else:
                messages.error(request, "Login failed. Please check your username and password again.")
                return redirect('Homeapp:client_login')
    else:
        form = LoginForm()

    return render(request, 'Homeapp/client_login.html', {'form': form})


def agent_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Create profile and set is_agent to True
            profile = Profile.objects.create(user=user, is_agent=True)

            # # Send welcome email
            # username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            # htmly = get_template('Homeapp/welcome_email.html')
            # context = {'username': username}
            # subject = 'Welcome to Our Platform!'
            # from_email = 'your_email@gmail.com'
            # to = email

            # html_content = htmly.render(context)
            # msg = EmailMultiAlternatives(subject, '', from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            messages.success(request, "Registration successful! Please log in.")
            return redirect('Homeapp:agent_login')
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect('Homeapp:agent_registration')
    else:
        form = RegistrationForm()

    return render(request, 'Homeapp/agent_registration.html', {'form': form})

# def agent_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
            
#             auth_agent = authenticate(request, username=username, password=password)  
            
#             if auth_agent is not None:
                
#                 login(request, auth_agent)
#                 messages.success(request, f'Welcome back, {username}!')
#                 return redirect('Agent:agent_home')  
#             else:
#                 messages.error(request, 'Invalid username or password. Please try again.')
#         else:
#             messages.error(request, 'Please correct the errors below.')

#     else:
#              form = LoginForm()

   
#     return render(request, 'Homeapp/agent_login.html', {'form': form})

def agent_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_agent = authenticate(request, username=username, password=password)

            if auth_agent is not None:
                profile = Profile.objects.get(user=auth_agent)

                if profile.is_agent:  # Check if the user is an agent
                    login(request, auth_agent)
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('Agent:agent_home')
                else:
                    messages.error(request, 'Only agents are allowed to log in here.')
                    return redirect('Homeapp:agent_login')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                return redirect('Homeapp:agent_login')
        else:
            messages.error(request, 'Please correct the errors below.')
            return redirect('Homeapp:agent_login')
    else:
        form = LoginForm()

    return render(request, 'Homeapp/agent_login.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('adminpanel:admin_home') 
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('Homeapp:admin_login')
    
    return render(request, 'Homeapp/admin_login.html')  

def generate_otp():
    return random.randint(100000, 999999) 
def forgot_password(request): 
    if request.method == 'POST':
        email = request.POST.get('email')
        
       
        # otp = generate_otp()
        # request.session['otp'] = otp
        # request.session['user_email'] = email

        
        # send_mail(
        #     subject='Your OTP Code',
        #     message=f'Your OTP code is {otp}.',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[email],
        # )

        messages.success(request, "An OTP has been sent to your email address.")
        return redirect('Homeapp:otp') 
    return render(request, 'Homeapp/forgot_password.html')

def otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            email = request.session.get('user_email')
            session_otp = request.session.get('otp')

            if entered_otp and session_otp and entered_otp == session_otp: 
                messages.success(request, "OTP verified. You can now reset your password.")
                return redirect('Homeapp:reset_password') 
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('Homeapp:otp')  

    else:
        form = OTPVerificationForm()  

    return render(request, 'Homeapp/otp.html', {'form': form}) 


def reset_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

      
        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return render(request, 'Homeapp/reset_password.html')

       
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return render(request, 'Homeapp/reset_password.html')

        user = request.user
        user.set_password(new_password)
        user.save()

       
        update_session_auth_hash(request, user)

        messages.success(request, "Your password has been updated successfully.")
        return redirect('Homeapp:client_login')  

    return render(request, 'Homeapp/reset_password.html')



def about(request):
    return render(request,'Homeapp/About.html')

def contact(request):
    if request.method == 'POST':
       
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

       
        if not fullname or not email or not subject or not message:
            messages.error(request, 'Please fill in all the required fields.')
        else:
            try:
              
                htmly = get_template('Homeapp/contact_email.html') 
                context = {'fullname': fullname, 'email': email, 'phone': phone, 'subject': subject, 'message': message}  
                email_subject = 'Contact Form Submission'
                from_email = 'your_email@gmail.com'  
                to = email  

              
                html_content = htmly.render(context)
                msg = EmailMultiAlternatives(email_subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, f'An error occurred while sending your message: {e}')

           
            return render(request, 'Homeapp/home.html') 

    return render(request, 'Homeapp/contact.html')

def property(request):
    return render(request,'Homeapp/property.html')

def services(request):
    return render(request,'Homeapp/services.html')

# def handler404(request, *args, **argv):
#     response = render_to_response('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render_to_response('500.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response