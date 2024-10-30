from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User



def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            'Welcome to Our Platform',
            f'Hello {user.username},\n\nThank you for registering with us. We hope you enjoy your experience!',
            'noreply@yourdomain.com', 
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass
@shared_task
def send_otp_email_task(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

@shared_task
def send_contact_email(fullname, email, phone, subject, message):
    full_message = f"From: {fullname} <{email}>\n\nPhone: {phone}\n\nMessage:\n{message}"
    send_mail(
        subject,
        full_message,
        email,
        ['miznamizz1@gmail.com'],
        fail_silently=False,
    )