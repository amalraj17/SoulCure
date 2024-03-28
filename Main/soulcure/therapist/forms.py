from django import forms
from .models import Therapy
# from .validators import allow_only_images_validator

class TherapyForm(forms.ModelForm):
    
    therapy_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Therapy Name',
                'id':'tname',
            }
        )
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg",
                "id":"duration",
                'placeholder': 'Enter Duration in weeks'
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':'4',
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter Breif Description',
                'id':'therapyDescription'
                }
            )
        )

    benefits = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':'3',
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter the benefits','id':'benefits',
                }
            )
        )
    fees = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg",
                "id":"fees",
                'placeholder': 'Enter Fees for a session'
            }
        )
    )

    class Meta:
        model = Therapy
        fields = ['therapy_name','description', 'duration','benefits','fees']



# forms.py


from django import forms
from .models import CustomUser, UserProfile, Therapist

# Define a custom widget class with Bootstrap styling for text inputs
class BootstrapTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control"
        super().__init__(*args, **kwargs)

# Define a custom widget class with Bootstrap styling for select fields
class BootstrapSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg"
        super().__init__(*args, **kwargs)


class BootstrapDateInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg"
        super().__init__(*args, **kwargs)

# Define a custom widget class with Bootstrap styling for textareas
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
        widget=BootstrapDateInput(attrs={'placeholder': 'YYYY-MM-DD', 'id': 'dob'})
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



class TherapistForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['bio', 'certification_name', 'certificate_id', 'experience', 'therapy']
        widgets = {
            'bio': BootstrapTextarea(attrs={'placeholder': 'Enter Bio' , 'id': 'bio'}),
            'certification_name': BootstrapTextInput(attrs={'placeholder': 'Enter Certification Name', 'id': 'certname'}),
            'certificate_id': BootstrapTextInput(attrs={'placeholder': 'Enter Certificate ID', 'id': 'certificationId'}),
            'experience': BootstrapTextInput(attrs={'placeholder': 'Enter Experience', 'id': 'experience'}),
            'therapy': BootstrapSelect(attrs={'placeholder': 'Select Therapy', 'id': 'therapy'}),
        }





###########################################################################################################################################

# Meeting Form

###########################################################################################################################################

# forms.py
from django import forms
from .models import TherapySessionSchedule

class TherapySessionForm(forms.ModelForm):
    class Meta:
        model = TherapySessionSchedule
        fields = [ 'meeting_url']
        widgets = {
           
            'meeting_url': forms.URLInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter the Meeting Url'
                
            }),
        }