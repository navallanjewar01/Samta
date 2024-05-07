
# users/urls.py
from django.urls import path
from .views import user_signup, all_users

urlpatterns = [
    path('signup/', user_signup, name='user_signup'),
    path('users/', all_users, name='all_users'),
]


