from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('admin-index/',views.adminindex,name='adminindex'),
    path('therapist-index/',views.therapistindex,name='therapist'),
    path('editor-index/',views.editorindex,name='editor'),
    path('about/',views.about,name='about'),
    path('familytherapy/',views.familytherapy,name='familytherapy'),
    path('chooseoption/',views.choosetherapy,name='chooseoption'), 
    path('get/menu/<str:filename>/', views.view_pdf, name='view_pdf'),




    path('deleteUser/<int:delete_id>',views.deleteUser,name="deleteUser"),
    path('updateStauts/<int:update_id>',views.updateStatus,name="updateStatus"),
]
