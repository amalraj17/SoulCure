from django.shortcuts import render,redirect, get_object_or_404
from .forms import TherapyForm
from .models import Therapy,LeaveRequest
from accounts.models import CustomUser,UserProfile
from .models import Therapist
from itertools import zip_longest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserForm, TherapistForm, UserProfileForm
from client.models import Appointment
from urllib.parse import urlparse, parse_qs
from datetime import date,datetime






# Create your views here.
@login_required
def addTherapy(request):
    if request.method == 'POST':
        form = TherapyForm(request.POST)
        if form.is_valid():
            therapy_name = form.cleaned_data['therapy_name']
            des = form.cleaned_data['description']
            duration = form.cleaned_data['duration']
            benefits = form.cleaned_data['benefits']
            fees = form.cleaned_data['fees']
            # Check if a therapy with the same name already exists
            if Therapy.objects.filter(therapy_name=therapy_name).exists():
                error_message = "Therapy with this name already exists."
            else:
                therapy = Therapy.objects.create(therapy_name=therapy_name, description=des, duration=duration, benefits=benefits,fees=fees)
                therapy.save()
                return redirect('index')  # Redirect to the index page after successful registration
        else:
            error_message = "Form is not valid."
    else:
        form = TherapyForm()
        error_message = None

    return render(request, 'add-therapy.html', {'form': form, 'error_message': error_message})


@login_required
def listTherapist(request):
    therapists = Therapist.objects.all()
    cuser = CustomUser.objects.filter(role=CustomUser.THERAPIST, id__in=therapists.values_list('user_id', flat=True))
    uprofile = UserProfile.objects.filter(user_id__in=cuser.values_list('id', flat=True))
    combined_data = list(zip_longest(cuser, uprofile, therapists))
    return render(request, 'demo2.html', {'combined_data': combined_data})


########################################################################################################################

#User-profile

########################################################################################################################

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
    paginator = Paginator(combined_data, per_page=8)  # Change '10' to the number of therapists per page you prefer

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Retrieve the therapists for the current page
    therapists_page = paginator.get_page(page_number)

    return render(request, 'therapist/therapists.html', {'therapists_page': therapists_page})

def family_therapists(request):
    # if Therapy.status == True:
        therapists = Therapist.objects.filter(therapy__id= 3)
        cuser = CustomUser.objects.filter(role=CustomUser.THERAPIST, id__in=therapists.values_list('user_id', flat=True))
        uprofile = UserProfile.objects.filter(user_id__in=cuser.values_list('id', flat=True))
        combined_data = list(zip_longest(cuser, uprofile, therapists))

        paginator = Paginator(combined_data, per_page=4)  
        page_number = request.GET.get('page')
        therapists_page = paginator.get_page(page_number)

        return render(request, 'therapist/family-therapist.html', {'therapists_page': therapists_page})
    # else:
        
    #     return render(request, 'index.html')





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
            pass 

    return redirect('view-appointment-therapist')


from .models import TherapySessionSchedule
from .forms import TherapySessionForm


from twilio.rest import Client
from django.conf import settings


def schedule_therapy_session(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if a therapy session is already scheduled for this appointment
    existing_session = TherapySessionSchedule.objects.filter(appointment=appointment).first()
    therapist = request.user
    meet_url = None
    therapistdata = Therapist.objects.get(user=therapist)
    meet_url = therapistdata.meeting_url
    print(therapist)


    if request.method == 'POST':
        form = TherapySessionForm(request.POST)
        if form.is_valid():
            if existing_session:
                return render(request, 'therapist/schedule-meeting.html', {
                    'form': form,
                    'appointment': appointment,
                    'error_message': 'A therapy session is already scheduled for this appointment.'
                })
            
            therapy_session = form.save(commit=False)
            therapy_session.platform = 'SoulCure'
            therapy_session.appointment = appointment
            therapy_session.status = 'scheduled'
            therapy_session.save()
            therapistdata.meeting_url = therapy_session.meeting_url
            therapistdata.save()
            appointment.status = 'scheduled'
            appointment.save()

            # Send WhatsApp notification
            send_whatsapp_notification(appointment,therapy_session)

            return redirect('view-appointment-therapist')
    else:
        if existing_session:
            return render(request, 'therapist/schedule-meeting.html', {
                'form': None,
                'appointment': appointment,
                'error_message': 'A therapy session is already scheduled for this appointment.'
            })
    form = TherapySessionForm()
    if meet_url is not None:
        form = TherapySessionForm(initial={'meeting_url': meet_url})
    print(form)

    return render(request, 'therapist/schedule-meeting.html', {'form': form, 'appointment': appointment})

def send_whatsapp_notification(appointment,therapy_session):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    to_number = 'whatsapp:+919074386935'  # Replace with the recipient's WhatsApp number
    date_formatted = appointment.date.strftime('%Y-%m-%d')
    time_slot = appointment.time_slot  # Make sure this is properly formatted
    platform = therapy_session.platform
    url = therapy_session.meeting_url

    parsed_url = urlparse(url)
    query_parameters = parse_qs(parsed_url.query)
    meeting_id = query_parameters.get('roomID')[0] if query_parameters.get('roomID') else None
    print(meeting_id) 
     
    message_body = (
    f"Dear client, we are pleased to inform you that your therapy session has been scheduled. \n\n"
    f"📅 Date: {date_formatted}\n"
    f"⏰ Time: {time_slot}\n"
    f"🌐 Platform: {platform}\n\n"  
    f"🔗 Please use the following link to join the meeting:\n\n"
    f"{url}\n\n"
    f"🔑 Meeting ID: {meeting_id}\n\n"
    f"⏱️ Be sure to join on time.\n\n\n"
    f"Thank you for choosing our services. "
    f"[Team SoulCure]"

    )
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to=to_number
        )
        print(f"WhatsApp notification sent to {to_number}: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp notification: {str(e)}")


from datetime import date as datetoday
from django.http import JsonResponse

@login_required
def view_appointment_therapist(request):
    therapist = request.user

    appointments = Appointment.objects.filter(therapist=therapist)

    for appointment in appointments:
        if appointment.date < datetoday.today() and appointment.status != 'completed':
            appointment.status = 'completed'
            appointment.save()

    # Fetch the updated list of appointments
    appointments = Appointment.objects.filter(therapist=therapist)

    return render(request, 'therapist/view-appointments.html', {'appointments': appointments})


def view_therapy_schedules(request):
    therapistid =  request.user.id
    today = date.today()
    time_now = datetime.now().time()    # Filter appointments for the therapist for today
    appointments_today = Appointment.objects.filter(therapist=therapistid,date=today,status='scheduled',time_slot__gte=time_now).order_by('time_slot')
    print(appointments_today)
    return render(request,'therapist/view-schedules.html',{'appointment':appointments_today})

def view_therapy_schedule(request,appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    current_schedule = TherapySessionSchedule.objects.get(appointment=appointment_id)
    print(current_schedule)

    if request.method == 'POST':
        meeturl = current_schedule.meeting_url
        print(meeturl)

        parsed_url = urlparse(meeturl)
        query_parameters = parse_qs(parsed_url.query)
        room_id = query_parameters.get('roomID', [None])[0]  # Get the first roomID parameter or None
        print(room_id)
        # Now you can use the room_id as needed

        # Redirect to dashboard with meeturl as a query parameter
        return HttpResponseRedirect(reverse('dashboard') + f'?roomID={room_id}')

    return render(request,'therapist/view-schedule.html',{'current_schedule':current_schedule,'appointment':appointment})


@login_required
def fetch_appointments(request):
    therapist = request.user
    status1 = request.GET.get('status')

    today = datetoday.today()

    if status1 == 'completed':
        appointments = Appointment.objects.filter(therapist=therapist, date__lt=today).exclude(status='not_paid')
    elif status1 == 'today':
        appointments = Appointment.objects.filter(therapist=therapist, date=today).exclude(status='not_paid')
    elif status1 == 'upcoming':
        appointments = Appointment.objects.filter(therapist=therapist, date__gt=today).exclude(status='not_paid')
    else:
        appointments = []

    data = []
    for appointment in appointments:
        data.append({
            'sl_no': appointment.id,
            'client': appointment.client.name,
            'appointment_date': appointment.date.strftime('%Y-%m-%d'),
            'time_slot': appointment.get_time_slot_display(),
            'status': appointment.get_status_display(),
        })

    return JsonResponse({'appointments': data})


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