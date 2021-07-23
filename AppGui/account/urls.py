from django.urls import path

from .views import profile, password

urlpatterns = [
    path('profile/', profile, name='AccountProfile'),
    path('password/', password, name='AccountPassword'),
]
