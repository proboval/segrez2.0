from django.contrib.auth.backends import BaseBackend
from .models import Company, Expert
from django.contrib.auth.models import User


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None): # поменять try на if, чтобы ускорить код
        try:
            user = Expert.objects.get(email=email)
        except Expert.DoesNotExist:
            try:
                user = Company.objects.get(email=email)
            except Company.DoesNotExist:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return None

        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return Expert.objects.get(pk=user_id)
        except Expert.DoesNotExist:
            try:
                return Company.objects.get(pk=user_id)
            except Company.DoesNotExist:
                try:
                    return User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return None
