from django.urls import path

from . import views

urlpatterns = [
    path('core/signup', views.RegistrationView.as_view(), name='signup'),
]