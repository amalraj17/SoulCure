from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from blogs.models import Posts
from client.models import QuestionnaireResponse

# Create your views here.


User = get_user_model


import razorpay
from django.conf import settings

# Initialize the Razorpay client


def index(request):
    if request.user.is_authenticated:
        if request.user.role == 4 and not request.path == reverse('adminindex'):
            return redirect(reverse('adminindex'))
        elif request.user.role == 2 and not request.path == reverse('therapist'):
            return redirect(reverse('therapist'))
        elif request.user.role == 3 and not request.path == reverse('editor'):
            return redirect(reverse('editor'))
        elif request.user.role == 1 and not request.path == reverse('index'):
            q_response = QuestionnaireResponse.objects.get(user=request.user)
            if q_response.questionnarie_done == False:
                return redirect(reverse('attend_questionnaire'))
            return redirect(reverse('index'))

    return render(request, 'index.html')


# def index(request):
#     if request.user.is_authenticated:
#         if request.user.role == 4 and not request.path == reverse('adminindex'):
#             return redirect(reverse('adminindex'))
#         elif request.user.role == 2 and not request.path == reverse('therapist'):
#             return redirect(reverse('therapist'))
#         elif request.user.role == 1 and not request.path == reverse('index'):
#             return redirect(reverse('index'))
    
#     return render(request, 'index.html', {'user': request.user})


@login_required
def adminindex(request):
    if request.user.is_authenticated:
        if request.user.role == 4 and not request.path == reverse('adminindex'):
            return redirect(reverse('adminindex'))
        elif request.user.role == 2 and not request.path == reverse('therapist'):
            return redirect(reverse('therapist'))
        elif request.user.role == 3 and not request.path == reverse('editor'):
            return redirect(reverse('editor'))
        elif request.user.role == 1 and not request.path == reverse('index'):
            q_response = QuestionnaireResponse.objects.get(user=request.user)
            if q_response.questionnarie_done == False:
                return redirect(reverse('attend_questionnaire'))
            return redirect(reverse('index'))
    # if request.user.role != 3 or (not request.path == reverse("adminindex")) :
    clients = CustomUser.objects.filter(role=CustomUser.CLIENT)
    client = clients.count()
    therapists = CustomUser.objects.filter(role=CustomUser.THERAPIST)
    therapist = therapists.count()
    activeuser = CustomUser.objects.filter(is_active=True)
    activeusers = activeuser.count()
    inactiveuser = CustomUser.objects.filter(is_active=False)
    inactiveusers = inactiveuser.count()
    users=CustomUser.objects.all()

    return render(request,'admin/admin-index.html',{'user':request.user,'client': client,'therapist': therapist,'users':users,'inactiveusers':inactiveusers,'activeusers':activeusers})
@login_required
def therapistindex(request):
    if request.user.is_authenticated:
        if request.user.role == 4 and not request.path == reverse('adminindex'):
            return redirect(reverse('adminindex'))
        elif request.user.role == 2 and not request.path == reverse('therapist'):
            return redirect(reverse('therapist'))
        elif request.user.role == 3 and not request.path == reverse('editor'):
            return redirect(reverse('editor'))
        elif request.user.role == 1 and not request.path == reverse('index'):
            q_response = QuestionnaireResponse.objects.get(user=request.user)
            if q_response.questionnarie_done == False:
                return redirect(reverse('attend_questionnaire'))
            return redirect(reverse('index'))
    return render(request,'therapist/therapist-index.html')


@login_required
def editorindex(request):
    if request.user.is_authenticated:
        if request.user.role == 4 and not request.path == reverse('adminindex'):
            return redirect(reverse('adminindex'))
        elif request.user.role == 2 and not request.path == reverse('therapist'):
            return redirect(reverse('therapist'))
        elif request.user.role == 3 and not request.path == reverse('editor'):
            return redirect(reverse('editor'))    
        elif request.user.role == 1 and not request.path == reverse('index'):
            q_response = QuestionnaireResponse.objects.get(user=request.user)
            if q_response.questionnarie_done == False:
                return redirect(reverse('attend_questionnaire'))
            return redirect(reverse('index'))

    cuser = request.user
    count = 0
    count = Posts.objects.filter(author=cuser).count()
    return render(request,'editor/index.html',{'count': count})



@login_required
def deleteUser(request,delete_id):
    delUser=CustomUser.objects.get(id=delete_id)
    delUser.delete()    
    return redirect('adminindex')

@login_required
def updateStatus(request,update_id):
    updateUser=CustomUser.objects.get(id=update_id)
    if updateUser.is_active==True:
        updateUser.is_active=False
    else:
        updateUser.is_active=True
    updateUser.save()
    return redirect('adminindex')

def about(request):
    return render(request,'about.html')

@login_required
def familytherapy(request):
    return render(request,'family-therapy.html')


@login_required
def choosetherapy(request):
    return render(request,'select-therapy.html')

