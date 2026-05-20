from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .enums import GENDER, IDENTITY_TYPE
from common.email import send_registration_emails
from common.models import TimeStampedModel
# Create your models here.

# Function to generate file path for user uploads
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename ="%s.%s" % (instance.user.id, filename)

    return "user_{0}/{1} ".format(instance.user.id, filename)

def generate_profile_pid():
    return f"PROF{uuid.uuid4().hex[:7].upper()}"

# Custom user model
class CustomUser(AbstractUser, TimeStampedModel):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER,default='other')
    otp = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.full_name or self.username
    


class Profile(TimeStampedModel):
    pid = models.CharField(max_length=25, unique=True, editable=False, default=generate_profile_pid)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')  
    full_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True,default='default_profile.png')
    
    
    
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    Address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER,default='other')
    identity_type = models.CharField(max_length=50, blank=True, null=True, choices=IDENTITY_TYPE,default='national_id')
    identity_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True,default='id.jpg')
    
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)

    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)
   


    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['-date']


    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.user.username    
    

    

# Signals to create or update user profile when user is created or updated
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        # send email
        send_registration_emails(instance)     
      


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()