from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from django.contrib  import messages,auth
from .models import CustomUser
# from accounts.backends import EmailBackend
from django.contrib.auth import get_user_model
from .forms import CustomUserForm, UserProfileForm
from .forms import TherapistForm

User = get_user_model()


def addTherapist(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        therapist_form = TherapistForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and therapist_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            therapist = therapist_form.save(commit=False)
            therapist.user = user
            therapist.user_profile = profile
            therapist.save()

            return redirect('index')  # Redirect to a success page or home

    else:
        user_form = CustomUserForm()
        profile_form = UserProfileForm()
        therapist_form = TherapistForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'therapist_form': therapist_form,  # Add the therapist form to the context
    }

    return render(request, 'add-therapist.html', context)

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

def register(request):
    if request.method == 'POST':
        name1 = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('pass', None)
        role = User.CLIENT

        if name1 and email and phone and password and role:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'register2.html', {'error_message': error_message})
            
            else:
                user = User(name=name1, email=email, phone=phone,role=role)
                user.set_password(password)  # Set the password securely
                user.save()
                return redirect('login')  
            
    return render(request, 'register2.html')

def userLogout(request):
    logout(request)
    return redirect('/')



