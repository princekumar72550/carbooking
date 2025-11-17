from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile

@login_required
def profile_view(request):
    """Display user profile information"""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None
    
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile_view(request):
    """Edit user profile information"""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        gender = request.POST.get('gender', '')
        
        # Update user information
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        # Update or create user profile
        if user_profile:
            user_profile.phone = phone
            user_profile.gender = gender
            user_profile.save()
        else:
            UserProfile.objects.create(
                user=user,
                phone=phone,
                gender=gender
            )
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'users/edit_profile.html', context)