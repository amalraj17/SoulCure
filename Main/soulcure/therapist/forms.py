from django import forms
from .models import Therapy
# from .validators import allow_only_images_validator

class TherapyForm(forms.ModelForm):
    
    therapy_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Therapy Name'
            }
        )
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg",
                "id":"phone",
                'placeholder': 'Enter Duration in weeks'
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':'4',
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter Breif Description'
                }
            )
        )

    benefits = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':'3',
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter the benefits'
                }
            )
        )


    class Meta:
        model = Therapy
        fields = ['therapy_name','description', 'duration','benefits']


