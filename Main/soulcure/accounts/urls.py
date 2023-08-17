from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
        # path('regform/',views.userRegister,name='regform'),
        path('login/',views.userlogin,name='login'),
        path('register/',views.register,name='register'),
        path('logout/',views.userLogout,name='logout'),
        path('',include('allauth.urls')),    
        path('add-therapist/',views.addTherapist,name='addTherapist'),
        path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
        path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
        path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
        path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
