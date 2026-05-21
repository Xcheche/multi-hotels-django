from django.shortcuts import render, redirect
from .models import CustomUser, Profile
from .forms import  RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.


def register(request):
    # If the user is already authenticated, 
    # redirect to home page or dashboard or use custom decorator to block access to registration page for authenticated users.
    if request.user.is_authenticated:
        return redirect("hotel:home")
    form = RegistrationForm(request.POST or None)  
    # Check if the form is valid
    if form.is_valid():
        created_user = form.save()  # Save the user to the database
        # Note: post_save signal automatically creates Profile and sends emails.
        # Otherwise, manually create profile here (uncomment below).
        # Note: This won't create profiles for superusers created via createsuperuser
        # command unless a signal is configured.
        # profile = Profile.objects.create(user=user)
        full_name = form.cleaned_data.get('full_name')
        phone_number = form.cleaned_data.get('phone_number')
        email = form.cleaned_data.get('email')
        
        # Authenticate and log in the user after registration
        authenticated_user = authenticate(
            request,
            email=email,
            password=form.cleaned_data.get('password1'),
        )
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Update profile with registration form data
        profile, _ = Profile.objects.get_or_create(user=created_user)
        profile.full_name = full_name
        profile.phone_number = phone_number
        profile.save()  # Save the profile with updated information

        if authenticated_user is not None:
            messages.success(request, "Registration successful. You are now logged in.")
        else:
            messages.success(request, "Registration successful. Please log in.")
        return redirect("hotel:home")  # Redirect to home page or dashboard after successful registration
    
    context = {'form': form}
    return render(request, "user_auth/register.html", context)