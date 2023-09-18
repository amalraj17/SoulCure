# forms.py

from django import forms
from .models import Appointment
from accounts.models import CustomUser

class BootstrapTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().__init__(*args, **kwargs)

# Define a custom widget class with Bootstrap styling for select fields
class BootstrapSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().__init__(*args, **kwargs)


class BootstrapDateInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg datepicker"
        super().__init__(*args, **kwargs)



class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'id': 'date','name':'date' ,'class': 'form-control form-control-lg', 'type': 'date'})
    )
    therapist_name = forms.CharField(
        max_length=100,  # Adjust the max length as needed
        required=False,  # Set to False to allow an empty field
        widget=forms.TextInput(attrs={'placeholder': 'Enter Therapist Name', 'id': '','class':'form-control form-control-lg bg-white','disabled':'disabled'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        

    class Meta:
        model = Appointment
        fields = [ 'therapist_name','date','time_slot']
        widgets = {
            'time_slot': BootstrapSelect(attrs={'placeholder': 'Select State', 'id': 'time_slot'}),
        }

class CurrentUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name','email','phone']
        widgets = {
            'name': BootstrapTextInput(attrs={'placeholder': 'Enter Your Name', 'id': 'name','disabled':'disabled'}),
            'email': BootstrapTextInput(attrs={'placeholder': 'Enter Your Email', 'id': 'email','disabled':'disabled'}),
            'phone': BootstrapTextInput(attrs={'placeholder': 'Enter Your Phone', 'id': 'phone'}),
        }


from django import forms
from accounts.models import CustomUser, UserProfile

class BootstrapTextarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg"
        kwargs["attrs"]["rows"] = 16  # Customize the number of rows as needed
        super().__init__(*args, **kwargs)

class BootstrapFileInput(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "custom-file-input"
        super().__init__(*args, **kwargs)

class BootstrapImageInput(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "custom-file-input"
        super().__init__(*args, **kwargs)

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': BootstrapTextInput(attrs={'placeholder': 'Enter Your Name', 'id': 'name'}),
            'email': BootstrapTextInput(attrs={'placeholder': 'Enter Your Email', 'id': 'email'}),
            'phone': BootstrapTextInput(attrs={'placeholder': 'Enter Your Phone', 'id': 'phone'}),
        }

class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(
        widget=BootstrapDateInput(attrs={'placeholder': 'YYYY-MM-DD', 'id': 'dobclient'})
    )

    profile_picture = forms.ImageField(
        widget=BootstrapImageInput(attrs={'id': 'pictureInput'})
    )
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address','addressline1', 'addressline2','country', 'state', 'city', 'pin_code', 'gender', 'dob']
        widgets = {
            # 'profile_picture': BootstrapFileInput(attrs={'placeholder': 'Upload Profile Picture'}),
            # 'profile_picture': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
            'address': BootstrapTextInput(attrs={'placeholder': 'Address Line 1', 'id': 'address'}),
            'addressline1': BootstrapTextInput(attrs={'placeholder': 'Address Line 2', 'id': 'address1'}),
            'addressline2': BootstrapTextInput(attrs={'placeholder': 'Address Line 3', 'id': 'address2'}),
            'country': BootstrapSelect(attrs={'placeholder': 'Select Country', 'id': 'country'}),
            'state': BootstrapSelect(attrs={'placeholder': 'Select State', 'id': 'state'}),
            'city': BootstrapTextInput(attrs={'placeholder': 'Enter City', 'id': 'city'}),
            'pin_code': BootstrapTextInput(attrs={'placeholder': 'Enter Pin Code', 'id': 'zipcode'}),
            'gender': BootstrapSelect(attrs={'placeholder': 'Select Gender', 'id': 'gender'}),
            # 'dob': forms.DateInput(attrs={'placeholder': 'Select Date of Birth', 'id': 'dob'}),
        }
