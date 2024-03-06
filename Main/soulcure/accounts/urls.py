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
        path('add-editors/',views.addEditors,name='add-editors'),
        path('view-therapies/', views.view_therapies, name='view-therapies'),
        path('users-lists/',views.users_list,name='users-lists'),
        path('change-therapy-status/<int:therapy_id>/', views.change_therapy_status, name='change-therapy-status'),
        path('update-therapy/<int:therapy_id>/', views.update_therapy, name='update-therapy'),
        path('susers/', views.susers, name='susers'),
        path('user-data/',views.user_data,name='user-data'),
        path('updateuserStauts/<int:update_id>',views.updateuserStatus,name="updateuserStatus"),
        path('view-appointments/',views.view_appointments,name='view-appointments'),
        path('view-leave-requests/',views.view_leave_requests,name='view-leave-requests'),
        path('admin_approve_reject_leave/<int:request_id>/', views.admin_approve_reject_leave, name='admin_approve_reject_leave'),
        # path('view-appointments/',views.view_appointments,name='view-appointments'),

       



        path('activate/<uidb64>/<token>', views.activate, name='activate'),
        path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
        path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
        path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
        path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]  
