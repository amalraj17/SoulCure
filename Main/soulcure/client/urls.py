from django.urls import path,include
from . import views


urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('edit-profile/',views.editprofile,name='edit-profile'),
    path('change-password-client/',views.change_password_client,name='change_password_client'),
    path('appointment/<int:t_id>/', views.appointment, name='appointment'),
]