from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from apps.users.models import UserProfile

def home(request):
    return render(request, 'core/home.html')

def login_view(request):
    # If user is already authenticated, redirect to home page
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user into Django's session-based authentication system
            django_login(request, user)
            
            # Redirect to next page or home page
            next_page = request.GET.get('next', '/')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'core/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        gender = request.POST.get('gender', '')
        profile_photo = request.FILES.get('profile_photo')
        
        # Validate form data
        errors = []
        
        # Check if all required fields are filled
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email:
            errors.append('Email is required')
        if not phone:
            errors.append('Phone number is required')
        if not password:
            errors.append('Password is required')
        if not password_confirm:
            errors.append('Password confirmation is required')
            
        # Validate email format
        if email:
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Invalid email format')
                
        # Check if email is already taken
        if email and User.objects.filter(email=email).exists():
            errors.append('Email is already registered')
            
        # Check if passwords match
        if password != password_confirm:
            errors.append('Passwords do not match')
            
        # Check password length
        if password and len(password) < 8:
            errors.append('Password must be at least 8 characters long')
            
        # If there are errors, display them
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'core/register.html')
            
        # Create user and profile
        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=email,  # Using email as username
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                
                # Create user profile
                user_profile = UserProfile.objects.create(
                    user=user,
                    phone=phone,
                    gender=gender if gender in ['male', 'female', 'other'] else '',
                )
                
                # Save profile photo if provided
                if profile_photo:
                    user_profile.profile_picture = profile_photo
                    user_profile.save()
                
                # Log the user in
                django_login(request, user)
                messages.success(request, 'Registration successful! Welcome to Car Booking System.')
                return redirect('home')
                
        except Exception as e:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'core/register.html')
    
    return render(request, 'core/register.html')

def logout_view(request):
    django_logout(request)
    return redirect('home')