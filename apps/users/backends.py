from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with either
    their username or email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')
        
        if username is None or password is None:
            return None
        
        # Check if the username is an email
        if '@' in username:
            # Try to find user by email
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                return None
        else:
            # Try to find user by username
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                # If not found by username, try by email as fallback
                try:
                    user = User.objects.get(email__iexact=username)
                except User.DoesNotExist:
                    return None
        
        # Check password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None