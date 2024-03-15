from email.message import EmailMessage
from io import BytesIO
from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import CustomUser,UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserForm, UserProfileForm
from therapist.models import Therapist,TherapistDayOff
from datetime import time
from .models import Appointment,FeedbackOption
from datetime import datetime
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from xhtml2pdf import pisa
import io






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

#Editor Profile

########################################################################################################################


@login_required
def profileeditor(request):
    
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

    return render(request, 'editor/profile.html', context)





@login_required
def editprofileeditor(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect('editorprofile')  # Redirect to the user's profile page after editing

    else:
        user_form = CustomUserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user_profile)
    print(user_profile.profile_picture)
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'user_profile':user_profile
    }

    return render(request, 'editor/edit-profile.html', context)

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
from django.conf import settings
from therapist.models import Therapy



@login_required
def book_appointment(request, t_id):
    therapist = get_object_or_404(CustomUser, id=t_id)
    print(therapist)
    current_therapists=Therapist.objects.filter(user=therapist)
    print(current_therapists)
    if current_therapists.exists():
        current_therapist = current_therapists.first()
        associated_therapy = current_therapist.therapy
        if associated_therapy:
            therapy_fee = associated_therapy.fees
            print("Therapy Fee:", therapy_fee)
        else:
            print("Therapist is not associated with any therapy.")
    else:
        print("Therapist not found.")

 

    context = None

    if request.method == 'POST':
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        # Check if the current user (client) has already booked an appointment for the same date and time slot
        existing_appointment = Appointment.objects.filter(client=request.user, date=date, time_slot=time_slot).exclude(time_slot__isnull=True).first()

        # Check if the current user (client) has already booked an appointment for the same date
        existing_appointment_same_date = Appointment.objects.filter(client=request.user, date=date).exclude(time_slot__isnull=True).first()

        # Check if the selected date is in the therapist's day-offs
        therapist_day_off = TherapistDayOff.objects.filter(therapist=therapist, date=date).first()

        if therapist_day_off:
            context = {
                'error': f'{therapist.name} is on leave on {date}. Please select a different date.',
                'therapist': therapist,
            }
        elif existing_appointment:
            apps = Appointment.objects.filter(date=date, time_slot=time_slot).exclude(time_slot__isnull=True)
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

                appointment1 = form.save(commit=False)  # Save the form data to the appointment instance but don't commit to the database yet
                appointment1.save()
                t_fee=int(therapy_fee)
                return redirect('payment',appointment_id=appointment1.id,t_fees=therapy_fee)
                
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
    user=request
    return render(request,'client/confirm-appointments.html')

def cancel_appointment(request,appointment_id):
    print("Entered")

    
    print(appointment_id)
    appo=Appointment.objects.get(id=appointment_id)
    appo.cancel_status=True
    appo.time_slot=None
    appo.status='cancelled'
    appo.save()
    return redirect('view-appointment-client')

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



from datetime import date as datetoday
from django.template.loader import render_to_string


def view_appointment_client(request):
    client = request.user

    active_appointments = Appointment.objects.filter(client=client)   
    return render(request,'client/view-appointments.html',{'appointments':active_appointments})

# def view_completed_appointment_client(request):
#     client = request.user
#     today = datetoday.today()

#     active_appointments = Appointment.objects.filter(client=client,date__lt=today)
       
#     return redirect('client/view-appointments.html',{'appointments':active_appointments})

from datetime import date as datetoday
from django.db.models import Q



def fetch_appointments_clients(request):
    client = request.user

    # Determine the status based on the request parameter
    status1 = request.GET.get('status')
    print(status1)

    # Get the current date
    today = datetoday.today()

    if status1 == 'completed':
        appointments = Appointment.objects.filter(client=client, date__lt=today,cancel_status=False)
    elif status1 == 'upcoming':
        # appointments = Appointment.objects.filter(client=client, date__gte=today).exclude(status='not_paid')
        appointments = Appointment.objects.filter(client=client, date__gte=today,cancel_status=False).exclude(status='not_paid')

        print(appointments)
    else:
        appointments = []

    data = []
    for appointment in appointments:
        data.append({
            'sl_no': appointment.id,
            'therapist': appointment.therapist.name,
            'appointment_date': appointment.date.strftime('%Y-%m-%d'),
            'time_slot': appointment.get_time_slot_display(),
            'status': appointment.get_status_display(),
        })

    return JsonResponse({'appointments': data})


# def get_appointments(request):
#     filter_type = request.GET.get("filter")
#     client = request.user
#     today = datetoday.today()

#     if filter_type == "completed":
#         appointments = Appointment.objects.filter(client=client, date__lt=today)
#     elif filter_type == "upcoming":
#         appointments = Appointment.objects.filter(client=client, date__gte=today)
#     else:
#         appointments = []

#     # Render the appointments using a template
#     appointments_html = render_to_string("client/view-appointments.html", {"appointments": appointments})

#     return JsonResponse({"appointments_html": appointments_html})


# @login_required
# def fetch_client_appointments(request):
#     client = request.user
#     status = request.GET.get('status')
#     print(status)

#     today = datetoday.today()

#     if status == 'completed':
#         appointments = Appointment.objects.filter(client=client, date__lt=today)
#         print(appointments)


#     else:
#         appointments = []

#     data = []
#     for appointment in appointments:
#         therapist_name = appointment.therapist.name  # Get therapist name
#         print(therapist_name)
#         data.append({
#             'sl_no': appointment.id,
#             'therapist': appointment.therapist.name,
#             'appointment_date': appointment.date.strftime('%Y-%m-%d'),
#             'time_slot': appointment.get_time_slot_display(),
#             'status': appointment.get_status_display(),
#         })

#     return JsonResponse({'appointments': data})
    

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









########################################################################################################################

#payment

########################################################################################################################

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import logging
from django.http import HttpResponseForbidden , HttpResponseNotFound , HttpResponse ,HttpResponseBadRequest
from io import BytesIO
from xhtml2pdf import pisa
from .models import *
from django.urls import reverse




# logger = logging.getLogger(__name__)

razorpay_client = razorpay.Client(
     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# def paymenthandler(request):
#     # only accept POST request.
#     if request.method == "POST":
        
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }

#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(params_dict)
#             payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
#             if result is not None:
#                 payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
#                 amount = int(payment.amount * 100)  # Convert Decimal to paise
                
#                     # capture the payment
#                 razorpay_client.payment.capture(payment_id, amount)
#                 payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

#                     # Update the order with payment ID and change status to "Successful"
#                 payment.payment_id = payment_id
#                 payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
#                 payment.save()

#                     # render success page on successful capture of payment
#                 return render(request, 'index.html')
                
#                     # if there is an error while capturing payment.
#                 payment.payment_status = Payment.PaymentStatusChoices.FAILED
#                 return render(request, 'paymentfail.html')
#             else:
#                 # if signature verification fails.
#                 payment.payment_status = Payment.PaymentStatusChoices.FAILED
#                 return render(request, 'paymentfail.html')    # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#         # if other than POST request is made.
#         return HttpResponseBadRequest()



@csrf_exempt
def paymenthandler(request, appointment_id):
    # Only accept POST requests.
    if request.method == "POST":
        # Get the required parameters from the POST request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        amount = int(payment.amount * 100)  # Convert Decimal to paise

        # Capture the payment.
        razorpay_client.payment.capture(payment_id, amount)
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

        # Update the order with payment ID and change status to "Successful."
        payment.payment_id = payment_id
        payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
        payment.save()

        try:
            update_appointment = Appointment.objects.get(id=appointment_id)
            print(update_appointment)
            update_appointment.status = 'pending'
            update_appointment.save()
        except Appointment.DoesNotExist:
            # Handle the case where the appointment with the given ID does not exist
            return HttpResponseBadRequest("Invalid appointment ID")
       
        # Render the success page on successful capture of payment.
        return render(request, 'client/payment_confirmation.html',{'appointment':update_appointment})

    else:
        update_appointment = Appointment.objects.get(id=appointment_id)
        update_appointment.payment_status = False
        update_appointment.save()

        # If other than POST request is made.
        return HttpResponseBadRequest()








def payment(request, appointment_id,t_fees):
    # Use get_object_or_404 to get the Subscription object based on sub_id
        # Retrieve subscription features from a specific Subscription instance
    # You may want to retrieve a specific subscription
    print(t_fees)
    t_fees = float(request.resolver_match.kwargs['t_fees'])
    print(t_fees)

    appointments = Appointment.objects.all()
    current_appointment = Appointment.objects.get(pk=appointment_id)
    # For Razorpay integration
    currency = 'INR'
    amount = t_fees  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise
    print(amount_in_paise)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('paymenthandler', args=[appointment_id])  # Define your callback URL here

    phone=current_appointment.client.phone
    print(phone)
    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        appointment=current_appointment
    )
    appointment=current_appointment
    # Prepare the context data
    context = {
        'user': request.user,
        'appointment':appointment,
        # 'therapy_fee':t_fees,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
        'phone':phone,
        
    }

    return render(request, 'client/razorpay_payment.html', context)


# @csrf_exempt
# def payment_confirmation(request, order_id):
#     try:
#         # Retrieve the appointment based on the order_id
@csrf_exempt
def paymenthandler(request, appointment_id):
    # Only accept POST requests.
    if request.method == "POST":
        # Get the required parameters from the POST request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
    # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        amount = int(payment.amount * 100)  # Convert Decimal to paise

        # Capture the payment.
        razorpay_client.payment.capture(payment_id, amount)
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

        # Update the order with payment ID and change status to "Successful."
        payment.payment_id = payment_id
        payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
        payment.save()

        try:
            update_appointment = Appointment.objects.get(id=appointment_id)
            print(update_appointment)
            update_appointment.status = 'pending'
            update_appointment.save()
            pay_amt= payment.amount
            payee = update_appointment.client.name
            email = update_appointment.client.email
            ap_date=update_appointment.date
            ap_time=update_appointment.time_slot
            therapist = update_appointment.therapist.name
            appointment_email(email,  payee, ap_date, ap_time, pay_amt,therapist,payment)
        except Appointment.DoesNotExist:
            # Handle the case where the appointment with the given ID does not exist
            return HttpResponseBadRequest("Invalid appointment ID")
       
        # Render the success page on successful capture of payment.
        return render(request, 'client/payment_confirmation.html',{'appointment':update_appointment})

    else:
        update_appointment = Appointment.objects.get(id=appointment_id)
        update_appointment.payment_status = False
        update_appointment.save()

        # If other than POST request is made.
        return HttpResponseBadRequest()




def appointment_email(email, payee, ap_date, ap_time, therapist,payment,pay_amt):
    subject = "Appointment Confirmation"

    formatted_time = ap_time.strftime('%I:%M %p')
    formatted_date = ap_date.strftime('%B %d, %Y')

    message = f"Dear {payee},\n\nWe are pleased to confirm your upcoming appointment with our therapist, {therapist}, scheduled for {formatted_date} at {formatted_time}.\n\nYour payment receipt is attached to this email for your reference.\n\nThank you for choosing our services. We look forward to providing you with the best care possible.\n\nBest regards,\nSoulCure Team"
    from_email = 'info.soulcure@gmail.com'
    recipient_list = [email]
    pdf_invoice = generate_pdf_invoice(payee, pay_amt, payment)
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(f"{payee}_invoice.pdf", pdf_invoice, 'application/pdf')
    email.send()

def generate_pdf_invoice(payee, pay_amt, payment):
    # Create a PDF document using xhtml2pdf
    template_path = "invoice.html"  # Replace with the path to your HTML template
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{payee}_invoice.pdf"'

    template = get_template(template_path)
    context = {
        'payee': payee,
        'amount': pay_amt,
        'payment':payment # Format the timestamp as desired
        }
    html = template.render(context)

    pdf_buffer = io.BytesIO()
    pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), pdf_buffer)

    pdf_content = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_content

def payment(request, appointment_id,t_fees):
    # Use get_object_or_404 to get the Subscription object based on sub_id
        # Retrieve subscription features from a specific Subscription instance
    # You may want to retrieve a specific subscription
    print(t_fees)
    t_fees = float(request.resolver_match.kwargs['t_fees'])
    print(t_fees)

    appointments = Appointment.objects.all()
    current_appointment = Appointment.objects.get(pk=appointment_id)
    # For Razorpay integration
    currency = 'INR'
    amount = t_fees  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise
    print(amount_in_paise)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('paymenthandler', args=[appointment_id])  # Define your callback URL here

    phone=current_appointment.client.phone
    print(phone)
    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        appointment=current_appointment
    )
    appointment=current_appointment
    # Prepare the context data
    context = {
        'user': request.user,
        'appointment':appointment,
        # 'therapy_fee':t_fees,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
        'phone':phone,
        
    } 

    return render(request, 'client/razorpay_payment.html', context)
#         appointment = Appointment.objects.get(order_id=order_id)

#         # Check if the appointment status is 'not_paid'
#         if appointment.status == 'not_paid':
#             # Update the appointment status to 'confirmed' since payment is successful
#             appointment.status = 'pending'
#             appointment.save()

#             # Render the payment confirmation page with appointment details
#             return render(request, 'client/payment_confirmation.html', {'appointment': appointment})
#         else:
#             # Handle cases where the appointment status is already 'confirmed' or 'cancelled'
#             appointment.payment_status = False
#             return HttpResponse('Payment Failed')

#     except Appointment.DoesNotExist:
#         # Handle cases where the appointment with the given order_id does not exist
#         logger.error(f"Appointment with order_id {order_id} does not exist")
#         return HttpResponse('Appointment DoesNotExist')
    


def generate_appointment_pdf(request, appointment_id):
    # Get the appointment object from the database
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Prepare context data to be passed to the template
    context = {
        'appointment': appointment,
        'client_name': appointment.client.name ,
        'client_address': appointment.client.address,
        'client_email': appointment.client.email,
        'lawyer_name': f"{appointment.lawyer.user.first_name} {appointment.lawyer.user.last_name}",
        'appointment_date': appointment.appointment_date,
        'appointment_id': appointment.id,
        'appointment_order_id': appointment.order_id,
        'appointment_time': appointment.time_slot,
        'amount': '1 INR',  # You can fetch this dynamically if needed
    }

    # Render the HTML template with the context
    pdf_html = render(request, 'receipt.html', context)

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF file
    pdf = pisa.pisaDocument(BytesIO(pdf_html.content), buffer)

    if not pdf.err:
        # Set the response content type and filename
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="appointment_{appointment.id}.pdf"'

        # Get the value of the BytesIO buffer and add it to the response
        pdf_data = buffer.getvalue()
        buffer.close()
        response.write(pdf_data)

        return response

    return HttpResponse('PDF generation error')








########################################################################################################################

            #View Schedule 

########################################################################################################################

from therapist.models import *
from django.http import HttpResponseRedirect

def view_therapy_schedule(request,appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    current_schedule = TherapySessionSchedule.objects.get(appointment=appointment_id)
    print(current_schedule)

    if request.method == 'POST':
        meeturl = current_schedule.meeting_url
        print(meeturl)
        # return redirect('dashboard',meeturl=meeturl)
        return HttpResponseRedirect(reverse('dashboard') + f'?meeturl={meeturl}')


    return render(request,'client/view-schedule.html',{'current_schedule':current_schedule,'appointment':appointment})


# User FeedBack

from .models import FeedbackQuestions, TherapySessionFeedbacks

# def feedback_form(request,app_id):
#     print(app_id)
#     ar=[]
#     que=FeedbackQuestions.objects.all()
#     for i in que:
#         obj=FeedbackOption.objects.filter(question_id=i.id)
#         ar.append(obj)
#     count=range(0,que.count())
#     print(range)
#     return render(request,'client/feedback.html',{'que':que,'ar':ar,'count':count})

from .models import TherapySessionFeedbacks

def feedback_view(request, app_id):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('option_'):
                question_index = key.split('_')[1]
                question_id = request.POST.get(f'question_id_{question_index}')
                print(f"Question ID: {question_id}, Option: {value}")
                appointment = Appointment.objects.get(pk=app_id)
                # Create a new TherapySessionFeedbacks object with the extracted data
                feedback = TherapySessionFeedbacks.objects.create(
                    question=FeedbackQuestions.objects.get(pk=question_id),
                    appointment=appointment,
                    Answer=value
                )
                

        return redirect('feedback_success')

    # If the request method is not POST, render the feedback form page
    questions_with_options = []
    questions = FeedbackQuestions.objects.all()
    for question in questions:
        options = FeedbackOption.objects.filter(question=question)
        question_dict = {
            'question': question,
            'options': options
        }
        questions_with_options.append(question_dict)

    return render(request, 'client/feedback.html', {'questions_with_options': questions_with_options})

def feedback_success(request):
    return render(request, 'client/feedback_success.html')


def add_questions(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        options = request.POST.getlist('options')

        # Create the FeedbackQuestions instance
        question = FeedbackQuestions.objects.create(question=question_text)
        print(options)
        # Create FeedbackOptions instances for each option
        for option_text in options:
            FeedbackOption.objects.create(question=question, option_text=option_text)

        # Redirect to therapist index after adding questions and options
        return redirect('http://127.0.0.1:8000/therapist-index/')

    return render(request, 'add_questions.html')