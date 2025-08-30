from django.utils.translation import gettext as _
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from loguru import logger





def send_otp_email(email, otp):
    """Send an OTP email to the user."""

    subject = _("Your Login OTP Code")
    recipient_list = [email]

    context = {
        "otp": otp,
        "expiry_time": settings.OTP_EXPIRATION,
        "site_name": settings.SITE_NAME,
    }

    html_email = render_to_string('emails/otp_email.html', context)
    plain_email = strip_tags(html_email) # Fallback for email clients that don't support HTML

    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_email,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list
    )
    email.attach_alternative(html_email, "text/html")

    try:
        email.send()
        logger.info(f"OTP email sent to: {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}. Error: {e}")
        # raise e



def send_account_locked_email(user):
    """Send an account locked email to the user."""

    subject = _("Your Account Has Been Locked")
    recipient_list = [user.email]

    context = {
        "user": user, 
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),  # Convert to minutes
        "site_name": settings.SITE_NAME,
    }

    html_email = render_to_string('emails/account_locked_email.html', context)
    plain_email = strip_tags(html_email)  # Fallback for email clients that don't support HTML

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_email,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list
    )
    email.attach_alternative(html_email, "text/html")

    try:
        email.send()
        logger.info(f"Account locked email sent to: {user.email}")
    except Exception as e:
        logger.error(f"Failed to send account locked email to {user.email}. Error: {e}")
        # raise e




