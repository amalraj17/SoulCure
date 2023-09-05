# from django import forms
# from .models import CustomUser
# # from .validators import allow_only_images_validator

# class UserForm(forms.ModelForm):

#     password = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             "class": "form-control form-control-lg",
#             "id":"pass",
#             'placeholder': 'Enter Password'}
#         ))
    
#     confirm_password = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             "class": "form-control form-control-lg",
#             "id":"cpass",
#             'placeholder': 'Confirm Password'}
#         ))
    
#     name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control form-control-lg",
#                 "id":"name",
#                 'placeholder': 'Enter Name'
#             }
#         )
#     )
#     phone = forms.CharField(
#         widget=forms.NumberInput(
#             attrs={
#                 "class": "form-control form-control-lg",
#                 "id":"phone",
#                 'placeholder': 'Enter Phone'
#             }
#         )
#     )
#     email=forms.EmailField(
#         widget=forms.EmailInput(
#             attrs={
#                 "class": "form-control form-control-lg",
#                 "id":"mail",
#                 'placeholder': 'Enter Email',
#                 }
#         )
#     )




#     class Meta:
#         model = CustomUser
#         fields = ['name','email', 'phone','password']
        
            
        

    
from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile
from therapist.models import Therapist

CustomUser = get_user_model()

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-lg",
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-lg",
        'placeholder': 'Confirm Password'
    }))
    
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "form-control form-control-lg ",
                'placeholder': 'Enter Name'
            }),
            'email': forms.EmailInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Email'
            }),
            'phone': forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Phone Number'
            }),
            # 'role': forms.Select(attrs={
            #     "class": "form-control form-control-lg"
            # }),

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        "class": "form-control form-control-lg",
        'placeholder': 'Enter Date of Birth'
    }))  

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address', 'country', 'state', 'city', 'pin_code', 'gender', 'dob']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={
                "class": "form-control form-control-lg"
            }),
            'address': forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Address'
            }),
            'country': forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Country'
            }),
            'state': forms.Select(attrs={
                "class": "form-control form-control-lg"
            }),
            'city': forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter City'
            }),
            'pin_code': forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Pin Code'
            }),
            'gender': forms.Select(attrs={
                "class": "form-control form-control-lg"
            }),
        }


class TherapistForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['bio', 'certification_name', 'certificate_id', 'experience', 'therapy']
        widgets = {
            'bio': forms.Textarea(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Bio'
            }),
            'certification_name': forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Certification Name'
            }),
            'certificate_id': forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Certificate ID'
            }),
            'experience': forms.NumberInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Experience'
            }),
            'therapy': forms.Select(attrs={
                "class": "form-control form-control-lg"
            }),
        }
    
    def save(self, commit=True, user=None, user_profile=None):
        instance = super().save(commit=False)
        instance.user = user
        instance.user_profile = user_profile

        if commit:
            instance.save()
        return instance
