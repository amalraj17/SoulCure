from django.urls import path,include
from . import views


urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('edit-profile/',views.editprofile,name='edit-profile'),
    path('change-password-client/',views.change_password_client,name='change_password_client'),
    path('appointment/<int:t_id>/', views.appointment, name='appointment'),
    path('get-available-time-slots/', views.get_available_time_slots, name='get-available-time-slots'),
    path('demosearch/',views.search_therapists,name="demosearch"),
    path('demosearch2/',views.search_therapists2,name="search_therapists2"),
    path('search/',views.search,name='search'),
    path('view-appointment-client/',views.view_appointment_client,name='view-appointment-client'),
    path('cancel-appointment/', views.cancel_appointment, name='cancel-appointment'),
    path('confirm-appointment/', views.confirmappointment, name='confirm-appointment'),
    path('fetch_appointments_clients/', views.fetch_appointments_clients, name='fetch_appointments_clients'),
    # path('view-completed-appointment-client/', views.view_completed_appointment_client, name='view-completed-appointment-client'),
    # path('get_appointments/', views.get_appointments, name='get_appointments'),
    path('payment-confirmation/<str:order_id>/', views.payment_confirmation, name='payment_confirmation'),






    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),


]