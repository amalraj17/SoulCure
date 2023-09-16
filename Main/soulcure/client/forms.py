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