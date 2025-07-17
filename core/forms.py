from django import forms
from .models import CustomUser

class KYCForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['id_document', 'selfie']
        widgets = {
            'id_document': forms.ClearableFileInput(attrs={'class': 'block w-full'}),
            'selfie':      forms.ClearableFileInput(attrs={'class': 'block w-full mt-4'}),
        }

