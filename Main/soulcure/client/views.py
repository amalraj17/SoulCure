from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import CustomUser,UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from therapist.forms import CustomUserForm, UserProfileForm
from therapist.models import Therapist
from datetime import time





########################################################################################################################

#User-profile

########################################################################################################################


@login_required
def profile(request):
    
    user = request.user

    # Initialize variables for user profile and therapist info
    user_profile = None
 
    if user.userprofile.user.role == 1:
        try:
            # Get the user profile information
            user_profile = UserProfile.objects.get(user=user.userprofile.user)
           
        except UserProfile.DoesNotExist:
            user_profile = None
            

    context = {
        'user': user,
        'user_profile': user_profile,  # User profile information
    }

    return render(request, 'client/profile.html', context)





@login_required
def editprofile(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect('therapistProfile')  # Redirect to the user's profile page after editing

    else:
        user_form = CustomUserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user_profile)
    print(user_profile.profile_picture)
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'user_profile':user_profile
    }

    return render(request, 'client/edit-profile.html', context)

########################################################################################################################

#Update password

########################################################################################################################


@login_required
def change_password_client(request):
    val = 0
    
    if request.method == 'POST':
        # Get the current user
        user = CustomUser.objects.get(email=request.user.email)
        
        # Get the new password and confirm password from the request
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords are empty
        if not new_password or not confirm_password:
            messages.error(request, 'Please fill in both password fields.')
            val = 2
        else:
            # Check if the passwords match
            if new_password == confirm_password:
                # Change the user's password
                user.set_password(new_password)
                user.save()
                # Update the session and log the user back in
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated.')
                val = 1
            else:
                messages.error(request, 'Passwords do not match.')

    return render(request, 'client/profile.html', {'msg': val})

########################################################################################################################

#Appointments

########################################################################################################################


from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm,CurrentUserForm


@login_required
def appointment(request,t_id):
    therapist = get_object_or_404(CustomUser, id=t_id)
    context=None
    print(t_id)
    print(therapist.name)
    if request.method == 'POST':
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        
        # Check if an appointment already exists for the selected date and time slot
        app = Appointment.objects.filter(therapist=therapist, date=date, time_slot=time_slot)
        
        if app.count() == 0:  # Use app.count() to check the count
            form = AppointmentForm(request.POST)
            form.instance.client = request.user
            form.instance.therapist = therapist
            
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            apps=Appointment.objects.filter(therapist=therapist,date=request.POST.get('date'))
            time_slots={time(9,0):1,time(11, 0):1,time(13,0):1,time(15, 0):1,time(17,0):1}
            for time_slot in time_slots:
                for app in apps:
                    if app.time_slot== time_slot:
                        time_slots[time_slot]=0
            available_slots=""
            for time_slot in time_slots:
                if time_slots[time_slot]==1:
                    available_slots+="\n"+time_slot.strftime('%I:%M %p')
            available_slots=available_slots.strip()
            user = request.user
            initial_data = {
            'client': user,
            'client_name': user.name,
            'client_phone': user.phone,
            'therapist':therapist.id,
            'therapist_name':therapist.name,
        }
            appointment_form = AppointmentForm(initial=initial_data)
            user_form = CurrentUserForm(instance=user)
            context={
                'error':'Therapist already shceduled on the selected Date and Time Slot',
                'therapist':therapist,
                'appointment_form': appointment_form,
                'user_form': user_form,
                'available_slots':available_slots
            }
            return render(request, 'appointment.html', context) 
    else:
        user = request.user
        initial_data = {
            'client': user,
            'client_name': user.name,
            'client_phone': user.phone,
            'therapist':therapist.id,
            'therapist_name':therapist.name,
        }
        appointment_form = AppointmentForm(initial=initial_data)
        user_form = CurrentUserForm(instance=user)
        context = {'appointment_form': appointment_form, 'user_form': user_form ,'therapist':therapist}
    
    return render(request, 'appointment.html', context)



########################################################################################################################

#Search

########################################################################################################################

def search(request):
    return render(request,'search.html')


from django.shortcuts import render
from django.http import JsonResponse
from therapist.models import Therapist


@login_required
def search_therapists(request):
        # Get search criteria from AJAX reques
    return render(request, 'demosearch.html')  # Replace 'search.html' with your template

from django.db.models import Q
@login_required
def search_therapists2(request):
    query = request.GET.get('query')

    # Use Q objects to filter therapists based on therapy name or therapist name
    therapists = Therapist.objects.filter(
        Q(user__name__icontains=query) | Q(therapy__therapy_name__icontains=query)
    )

    therapists_data = [
        {
            'id': therapist.user.id,
            'name': therapist.user.name,
            'therapy': therapist.therapy.therapy_name,
            'profile_picture': therapist.user.userprofile.profile_picture.url,
            'experience': therapist.experience,
            'certification_name': therapist.certification_name,
        }
        for therapist in therapists
    ]

    return JsonResponse({'therapists': therapists_data})
