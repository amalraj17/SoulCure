from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import CustomUser,UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserForm, UserProfileForm
from therapist.models import Therapist,TherapistDayOff
from datetime import time
from .models import Appointment





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
from datetime import date as c_date


@login_required
def appointment(request, t_id):
    therapist = get_object_or_404(CustomUser, id=t_id)
    context = None

    if request.method == 'POST':
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        # Check if the current user (client) has already booked an appointment for the same date and time slot
        existing_appointment = Appointment.objects.filter(client=request.user, date=date, time_slot=time_slot).first()

        # Check if the current user (client) has already booked an appointment for the same date
        existing_appointment_same_date = Appointment.objects.filter(client=request.user, date=date).first()

        # Check if the selected date is in the therapist's day-offs
        therapist_day_off = TherapistDayOff.objects.filter(therapist=therapist, date=date).first()

        if therapist_day_off:
            context = {
                'error': f'The therapist is on leave on {date}. Please select a different date.',
                'therapist': therapist,
            }
        elif existing_appointment:
            apps = Appointment.objects.filter(date=date, time_slot=time_slot)
            time_slots = {time(9, 0): 1, time(11, 0): 1, time(13, 0): 1, time(15, 0): 1, time(17, 0): 1}
            for app in apps:
                time_slots[app.time_slot] = 0

            available_slots = [time_slot.strftime('%I:%M %p') for time_slot, available in time_slots.items() if available]
            available_slots = ", ".join(available_slots)

            user = request.user
            initial_data = {
                'client': user,
                'client_name': user.name,
                'client_phone': user.phone,
                'therapist': therapist.id,
                'therapist_name': therapist.name,
            }
            appointment_form = AppointmentForm(initial=initial_data, therapist_leave_dates=[])
            user_form = CurrentUserForm(instance=user)
            context = {
                'error': 'You have already scheduled an appointment for the selected Date and Time Slot',
                'therapist': therapist,
                'appointment_form': appointment_form,
                'user_form': user_form,
                'available_slots': available_slots
            }
        elif existing_appointment_same_date:
            user = request.user
            initial_data = {
                'client': user,
                'client_name': user.name,
                'client_phone': user.phone,
                'therapist': therapist.id,
                'therapist_name': therapist.name,
            }
            appointment_form = AppointmentForm(initial=initial_data, therapist_leave_dates=[])
            user_form = CurrentUserForm(instance=user)
            context = {
                'error': 'You have already scheduled an appointment for the selected Date',
                'therapist': therapist,
                'appointment_form': appointment_form,
                'user_form': user_form,
            }
        else:
            form = AppointmentForm(request.POST, therapist_leave_dates=[])
            form.instance.client = request.user
            form.instance.therapist = therapist

            if form.is_valid():
                form.save()
                return redirect('confirm-appointment')

    else:
        user = request.user
        initial_data = {
            'client': user,
            'client_name': user.name,
            'client_phone': user.phone,
            'therapist': therapist.id,
            'therapist_name': therapist.name,
        }
        current_date = c_date.today()
        leave_dates = [str(date) for date in TherapistDayOff.objects.filter(therapist=therapist, date__gte=current_date).values_list('date', flat=True)]        
        appointment_form = AppointmentForm(initial=initial_data, therapist_leave_dates=leave_dates)
        user_form = CurrentUserForm(instance=user)

        context = {'appointment_form': appointment_form, 'user_form': user_form, 'therapist': therapist, 'leave_dates': leave_dates}

    return render(request, 'appointment.html', context)



def confirmappointment(request): 
    return render(request,'client/confirm-appointments.html')

def cancel_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            
            # Check if the appointment is not already canceled
            if appointment.status != 'Canceled':
                appointment.status = 'Canceled'
                appointment.delete() 
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Appointment is already canceled.'})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Appointment not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def get_available_time_slots(request):
    therapist_id = request.GET.get('therapist_id')
    therapist = get_object_or_404(CustomUser, id=therapist_id)
    date = request.GET.get('date')

    # Fetch existing appointments for the selected date and therapist
    existing_appointments = Appointment.objects.filter(therapist=therapist, date=date)

    # Create a list of all available time slots
    all_time_slots = [time(9, 0), time(11, 0), time(13, 0), time(15, 0), time(17, 0)]

    # Initialize a dictionary to store the availability of time slots
    time_slot_availability = {time_slot: True for time_slot in all_time_slots}

    # Mark time slots as unavailable if they are already booked
    for appointment in existing_appointments:
        if appointment.time_slot in time_slot_availability:
            time_slot_availability[appointment.time_slot] = False

    # Filter the available time slots
    available_time_slots = [time_slot.strftime('%I:%M %p') for time_slot, is_available in time_slot_availability.items() if is_available]

    return JsonResponse({'available_time_slots': available_time_slots})






def view_appointment_client(request):
    client = request.user

    active_appointments = Appointment.objects.filter(client=client)
    return render(request,'client/view-appointments.html',{'appointments':active_appointments})
    

########################################################################################################################

#Search

########################################################################################################################

def search(request):
    return render(request,'search.html')


from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from therapist.models import Therapist


@login_required
def search_therapists(request):
    return render(request, 'demosearch.html')  


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
