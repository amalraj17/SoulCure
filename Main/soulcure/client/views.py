from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import CustomUser,UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from therapist.forms import CustomUserForm, UserProfileForm






########################################################################################################################

#User-profile

########################################################################################################################


@login_required
def profile(request):
    
    # Retrieve the logged-in user's information
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

