from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

User = get_user_model
# Create your views here.
def index(request):
    clients = CustomUser.objects.filter(role=CustomUser.CLIENT)
    client = clients.count()
    therapists = CustomUser.objects.filter(role=CustomUser.THERAPIST)
    therapist = therapists.count()
    users=CustomUser.objects.all()

    return render(request,'index.html',{'user':request.user,'client': client,'therapist': therapist,'users':users})
def deleteUser(request,delete_id):
    delUser=CustomUser.objects.get(id=delete_id)
    delUser.delete()
    return redirect('/')
def updateStatus(request,update_id):
    updateUser=CustomUser.objects.get(id=update_id)
    if updateUser.is_active==True:
        updateUser.is_active=False
    else:
        updateUser.is_active=True
    updateUser.save()
    return redirect('/')