from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.RegistrationView.as_view(), name='signup'),
]