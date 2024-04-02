from django.urls import path,include
from . import views


urlpatterns = [
    path('editor-profile/',views.profileeditor,name='editorprofile'),
    path('edit-profile-editor/',views.editprofileeditor,name='edit-profile-editor'),
    path('profile/',views.profile,name='profile'),
    path('edit-profile/',views.editprofile,name='edit-profile'),
    path('change-password-client/',views.change_password_client,name='change_password_client'),
    path('appointment/<int:t_id>/', views.book_appointment, name='appointment'),
    path('get-available-time-slots/', views.get_available_time_slots, name='get-available-time-slots'),
    path('demosearch/',views.search_therapists,name="demosearch"),
    path('demosearch2/',views.search_therapists2,name="search_therapists2"),
    path('search/',views.search,name='search'),
    path('view-appointment-client/',views.view_appointment_client,name='view-appointment-client'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel-appointment'),
    path('confirm-appointment/', views.confirmappointment, name='confirm-appointment'),
    path('fetch_appointments_clients/', views.fetch_appointments_clients, name='fetch_appointments_clients'),
    path('view_therapy_schedule/<int:appointment_id>/', views.view_therapy_schedule, name='view_therapy_schedule'),
    path('view_therapy_schedule_ag/', views.view_therapy_schedule_ag, name='view_therapy_schedule_ag'),

    # path('feedback/<int:app_id>',views.feedback_form,name='feedback'),
    path('feedbackk/<int:app_id>',views.feedback_view,name='feedbackk'),
    path('feedback/view/',views.view_feedback_questions,name='feedback_view'),
    path('feedback/success/',views.feedback_success, name='feedback_success'),
    path('add_questions/',views.add_questions, name='add_questions'),
    path('add_questions_questionnaire/',views.add_questions_questionnaire, name='add_questions_questionnaire'),
    path('view_questionnaire/',views.view_questionnaire,name='view_questionnaire'),
    path('attend_questionnaire/',views.attend_questionnaire,name='attend_questionnaire'),
    path('recommended_therapist/',views.recommended_therapist,name='recommended_therapist'),







    # path('view-completed-appointment-client/', views.view_completed_appointment_client, name='view-completed-appointment-client'),
    # path('get_appointments/', views.get_appointments, name='get_appointments'),
    # path('payment-confirmation/<str:order_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('generate-pdf/<int:appointment_id>/', views.generate_appointment_pdf, name='generate_appointment_pdf'),
    path('payment/<int:appointment_id>/<str:t_fees>/', views.payment, name='payment'),
 





    path('paymenthandler/<int:appointment_id>/', views.paymenthandler, name='paymenthandler'),


]