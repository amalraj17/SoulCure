from django.urls import path,include
from . import views


urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('edit-profile/',views.editprofile,name='edit-profile'),
   

]