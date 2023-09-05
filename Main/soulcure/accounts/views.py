from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from django.contrib  import messages,auth
from .models import CustomUser,UserProfile
from therapist.models import Therapist
# from accounts.backends import EmailBackend
from django.contrib.auth import get_user_model
from .forms import CustomUserForm, UserProfileForm
from .forms import TherapistForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
from .tokens import account_activation_token

########################################################################################################################

#User Reg and Login with acc activation , logout

########################################################################################################################

User = get_user_model()

def activate(request, uidb64, token):
    print("Reached the activate view")
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        print("Token is valid") 
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('index')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("email/account-activation.html", {
        'user': user.name,
        'domain': 'localhost:8000',
        # 'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)  # Print the email for debugging
        print(password)  # Print the password for debugging

        if email and password:
            user = authenticate(request, email=email, password=password)
            print("Authenticated user:", user)  # Print the user for debugging
            if user is not None:
                auth_login(request, user)
                print("User authenticated:", user.email, user.role)
                return redirect('http://127.0.0.1:8000/')
            else:
                error_message = "Invalid login credentials."
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = "Please fill out all fields."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')
@user_not_authenticated
def register(request):
    if request.method == 'POST':
        name1 = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('pass', None)
        confirm_password = request.POST.get('cpass', None)
        role = User.CLIENT

        if name1 and email and phone and password and role:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'register2.html', {'error_message': error_message})
            
            elif password!=confirm_password:
                error_message = "Password's Don't Match, Enter correct Password"
                return render(request, 'register2.html', {'error_message': error_message})

            
            else:
                user = User(name=name1, email=email, phone=phone,role=role)
                user.set_password(password)  # Set the password securely
                user.is_active=False
                user.save()
                user_profile = UserProfile(user=user)
                user_profile.save()
                activateEmail(request, user, email)
                return redirect('login')  
            
    return render(request, 'register2.html')

def userLogout(request):
    logout(request)
    return redirect('/')




########################################################################################################################

#Add Therapist

########################################################################################################################

@login_required
def addTherapist(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']

            # Send welcome email
            send_welcome_email(user.email, password, user.name)

            user.set_password(password)
            user.is_active = True

            user.role = CustomUser.THERAPIST  # Set the role to "Therapist"
            user.save()

            # Check if the user has the role=2 (Therapist)
            if user.role == CustomUser.THERAPIST:
                therapist = Therapist(user=user)  # Create a Therapist instance
                therapist.save()

            user_profile = UserProfile(user=user)
            user_profile.save()

            return redirect('index')

    else:
        user_form = CustomUserForm()

    context = {
        'user_form': user_form,
    }

    return render(request, 'add-therapist.html', context)



def send_welcome_email(email, password, therapist_name):

    login_url = 'http://127.0.0.1:8000/accounts/login/'  # Update with your actual login URL
    login_button = f'Click here to log in: {login_url}'


    subject = 'SoulCure - Therapist Registration'
    message = f"Hello {therapist_name},\n\n"
    message += f"Welcome to SoulCure, your platform for holistic wellness and healing. We are thrilled to have you on board as a part of our dedicated team of therapists.\n\n"
    message += f"Your registration is complete, and we're excited to have you join us. Here are your login credentials:\n\n"
    message += f"Email: {email}\nPassword: {password}\n\n"
    message += "Please take a moment to log in to your account using the provided credentials. Once you've logged in, we encourage you to reset your password to something more secure and memorable.\n\n"
    message += login_button
    message += "\n\nSoulCure is committed to providing a safe and supportive environment for both therapists and clients. Together, we can make a positive impact on the lives of those seeking healing and guidance.\n"
    message += "Thank you for joining the SoulCure community. We look forward to your contributions and the positive energy you'll bring to our platform.\n\n"
    message += "Warm regards,\nThe SoulCure Team\n\n"
    


    from_email='amalraj89903@gmail.com'
      # Replace with your actual email
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)

