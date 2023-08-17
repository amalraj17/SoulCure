from django.shortcuts import render,redirect
from .forms import TherapyForm
from .models import Therapy
from accounts.models import CustomUser,UserProfile
from .models import Therapist
from itertools import zip_longest

# Create your views here.
def addTherapy(request):
    if request.method == 'POST':
        form = TherapyForm(request.POST)
        if form.is_valid():
            therapy_name = form.cleaned_data['therapy_name']
            des = form.cleaned_data['description']
            duration = form.cleaned_data['duration']
            benefits = form.cleaned_data['benefits']
            therapy = Therapy.objects.create(therapy_name=therapy_name, description=des, duration=duration, benefits=benefits)
            therapy.save()
            return redirect('index')  # Redirect to login page after successful registration
    else:
        form = TherapyForm()
    return render(request, 'add-therapy.html', {'form': form})


# from itertools import zip_longest
# from .models import CustomUser, UserProfile, Therapist

def listTherapist(request):
    therapists = Therapist.objects.all()
    cuser = CustomUser.objects.filter(role=CustomUser.THERAPIST, id__in=therapists.values_list('user_id', flat=True))
    uprofile = UserProfile.objects.filter(user_id__in=cuser.values_list('id', flat=True))
    combined_data = list(zip_longest(cuser, uprofile, therapists))
    return render(request, 'demo2.html', {'combined_data': combined_data})


# def profile(request):
#     return render(request,)

# def demo(request):
#     return render(request,'')
