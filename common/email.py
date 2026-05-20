from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_registration_emails(user):
    
    # ================= USER EMAIL =================
    subject_user = "Welcome to Multi Hotels!"
    
    context_user = {
        "user": user,
    }

    text_content_user = "Your account has been created successfully."
    html_content_user = render_to_string("emails/user_welcome.html", context_user)

    email_user = EmailMultiAlternatives(
        subject_user,
        text_content_user,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email_user.attach_alternative(html_content_user, "text/html")
    email_user.send()


    # ================= ADMIN EMAIL =================
    subject_admin = "New User Registered"

    context_admin = {
        "user": user,
    }

    text_content_admin = f"New user registered: {user.email}"
    html_content_admin = render_to_string("emails/admin_notification.html", context_admin)

    email_admin = EmailMultiAlternatives(
    subject_admin,
    text_content_admin,
    settings.DEFAULT_FROM_EMAIL,
    settings.ADMIN_EMAILS,   # ✅ directly pass list
)

    email_admin.attach_alternative(html_content_admin, "text/html")
    email_admin.send()