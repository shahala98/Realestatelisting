
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail


def send_welcome_email_task(user_email, username):
    """
    Function to send a welcome email to the user.
    
    Args:
        user_email (str): The recipient's email address.
        username (str): The recipient's username for personalization.
    """
    
    subject = 'Welcome to Our Platform!'

    from_email = settings.DEFAULT_FROM_EMAIL
    
    context = {
        'username': username,
    }

    html_content = render_to_string('welcome_email.html', context)
    text_content = f"Hi {username}, Welcome to Our Platform!\nWe're glad to have you with us."
    email_message = EmailMultiAlternatives(subject, text_content, from_email, [user_email])
    email_message.attach_alternative(html_content, "text/html")

    email_message.send()


def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}. It is valid for a short period of time.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")


def send_contact_email(fullname, email, phone, subject, message):
    """
    Sends a contact email to a predefined recipient.

    Args:
        fullname (str): The name of the sender.
        email (str): The email address of the sender.
        phone (str): The phone number of the sender.
        subject (str): The subject of the email.
        message (str): The message body of the email.
    """
    full_message = f"From: {fullname} <{email}>\n\nPhone: {phone}\n\nMessage:\n{message}"

    try:
        send_mail(
            subject,                          # Subject of the email
            full_message,                     # Message body
            email,                            # From email address
            ['miznamizz1@gmail.com'],         # Recipient email address
            fail_silently=False,              # Raise an error if email fails to send
        )
    except Exception as e:
        raise Exception(f"An error occurred while sending the email: {e}")



