from django.shortcuts import render,redirect, get_object_or_404
from .forms import TherapyForm
from .models import Therapy,LeaveRequest
from accounts.models import CustomUser,UserProfile
from .models import Therapist
from itertools import zip_longest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserForm, TherapistForm, UserProfileForm,MeetingScheduleForm
from client.models import Appointment








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

def listTherapist(request):
    therapists = Therapist.objects.all()
    cuser = CustomUser.objects.filter(role=CustomUser.THERAPIST, id__in=therapists.values_list('user_id', flat=True))
    uprofile = UserProfile.objects.filter(user_id__in=cuser.values_list('id', flat=True))
    combined_data = list(zip_longest(cuser, uprofile, therapists))
    return render(request, 'demo2.html', {'combined_data': combined_data})


########################################################################################################################

#User-profile

########################################################################################################################
def therapist_profile(request, therapist_id):
    try:
        therapist = Therapist.objects.get(id=therapist_id)
    except Therapist.DoesNotExist:
        # Handle the case where the therapist with the specified ID does not exist
        # You can redirect or show an error message
        therapist = None

    if therapist:
        user_profile = therapist.user.userprofile

        context = {
            'therapist': therapist,
            'user_profile': user_profile,
        }

        return render(request, 'therapist-profile2.html', context)

@login_required
def therapistprofile(request):
    
    # Retrieve the logged-in user's information
    user = request.user

    # Initialize variables for user profile and therapist info
    user_profile = None
    therapist_info = None
    if user.userprofile.user.role == 1:
        return redirect("profile")
    # Check if the user has a therapist role (role == 2)
    elif user.userprofile.user.role == 2:
        try:
            # Get the user profile information
            user_profile = UserProfile.objects.get(user=user.userprofile.user)
            # Get the therapist's specific information
            therapist = Therapist.objects.get(user=user.userprofile.user)

            # Include all fields from the Therapist model in therapist_info
            therapist_info = {
                'bio': therapist.bio,
                'certification_name': therapist.certification_name,
                'certificate_id': therapist.certificate_id,
                'experience': therapist.experience,
                'therapy': therapist.therapy,
            }
        except UserProfile.DoesNotExist or Therapist.DoesNotExist:
            user_profile = None
            therapist_info = None

    context = {
        'user': user,
        'user_profile': user_profile,  # User profile information
        'therapist_info': therapist_info,  # Therapist-specific information
    }

    return render(request, 'therapist-profile.html', context)



@login_required
def edit_therapist_profile(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    therapist = Therapist.objects.get(user=user)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        therapist_form = TherapistForm(request.POST, instance=therapist)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and therapist_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            therapist_form.save()
            user_profile_form.save()
            return redirect('therapistProfile')  # Redirect to the user's profile page after editing

    else:
        user_form = CustomUserForm(instance=user)
        therapist_form = TherapistForm(instance=therapist)
        user_profile_form = UserProfileForm(instance=user_profile)
    context = {
        'user_form': user_form,
        'therapist_form': therapist_form,
        'user_profile_form': user_profile_form,
        'user_profile':user_profile
    }

    return render(request, 'edit-therapist-profile.html', context)

########################################################################################################################

#Update password

########################################################################################################################


@login_required
def change_password(request):
    val=0
    if request.method == 'POST':
        # Get the current user
        user = CustomUser.objects.get(email=request.user.email)
        print(user.email)
        # Get the new password from the request
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords match
        if new_password == confirm_password:
            # Change the user's password
            print(new_password)
            user.set_password(new_password)
            user.save()
            print("pass is saved")
            # Update the session and log the user back in
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Your password was successfully updated.')
            val=1
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'therapist-profile.html',{'msg':val})  

########################################################################################################################

#View therapist

########################################################################################################################

@login_required
def viewtherapist(request, user_id):
    users = get_object_or_404(CustomUser, id=user_id)
    therapist = Therapist.objects.get(user=users)
    profile = UserProfile.objects.get(user=users)

    context={
        'users' : users,
        'userprofile' : profile,
        'therapist' : therapist
        }
    return render(request, 'therapist/view-therapist.html', context)


from django.core.paginator import Paginator

def therapists(request):
    therapists = Therapist.objects.all()
    cuser = CustomUser.objects.filter(role=CustomUser.THERAPIST, id__in=therapists.values_list('user_id', flat=True))
    uprofile = UserProfile.objects.filter(user_id__in=cuser.values_list('id', flat=True))
    combined_data = list(zip_longest(cuser, uprofile, therapists))

    # Create a Paginator object with a specified number of therapists per page
    paginator = Paginator(combined_data, per_page=4)  # Change '10' to the number of therapists per page you prefer

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Retrieve the therapists for the current page
    therapists_page = paginator.get_page(page_number)

    return render(request, 'therapist/therapists.html', {'therapists_page': therapists_page})




########################################################################################################################

#Appointments

########################################################################################################################

@login_required
def update_appointment_status(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        new_status = request.POST.get('status')
        print(appointment_id)
        print(new_status)

        try:
            appointment = Appointment.objects.get(id=appointment_id)

            if request.user == appointment.therapist:
                appointment.status = new_status
                appointment.save()
                return redirect('view-appointment-therapist')
            else:
                pass
        except Appointment.DoesNotExist:
            # Handle appointment not found
            pass 

    return redirect('view-appointment-therapist')


# from django.shortcuts import render, redirect
# from .forms import MeetingScheduleForm  # Import your MeetingScheduleForm or create one
# from .models import Appointment  # Import your Appointment model or adjust the import

# def schedule_meeting(request, appointment_id):
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#     except Appointment.DoesNotExist:
#         # Handle appointment not found
#         messages.error(request, 'Appointment not found.')
#         return redirect('view-appointment-therapist')

#     if request.method == 'POST':
#         form = MeetingScheduleForm(request.POST)
#         if form.is_valid():
#             meeting = form.save(commit=False)
#             meeting.appointment = appointment
#             meeting.save()
#             messages.success(request, 'Meeting scheduled successfully.')
#             return redirect('view-appointment-therapist')

#     else:
#         form = MeetingScheduleForm()

#     context = {
#         'form': form,
#         'appointment': appointment,
#     }

#     return render(request, 'therapist/schedule_meeting_modal.html', context)



@login_required
def view_appointment_therapist(request):
    therapist = request.user

    appointments = Appointment.objects.filter(therapist=therapist)
    return render(request,'therapist/view-appointments.html',{'appointments':appointments})




########################################################################################################################

#Leave

########################################################################################################################

@login_required
def leave_request(request):
    user = request.user  # Get the current user

   
    if user.is_authenticated and user.role == 2:
        lawyer_profile = Therapist.objects.get(user=user)  

        if request.method == 'POST':
            leave_date = request.POST.get('leave_date')

            # Check if the date is not already marked as a holiday
            if not LeaveRequest.objects.filter(therapist=user, date=leave_date).exists():
                # Create a holiday request
                leave_request = LeaveRequest(therapist=user, date=leave_date)
                leave_request.save()
                messages.success(request, 'Holiday request sent for review.')
            else:
                messages.warning(request, 'You have applied leave for this date Already,Kindly wait for the Status.')

        
        leave_requests = LeaveRequest.objects.filter(therapist=user)

        context = {
            'leave_requests': leave_requests,
        }
        return render(request, 'therapist/leave.html', context)

    else:
        messages.error(request, 'Only Therapist can request holidays.')
        return redirect('/')  #