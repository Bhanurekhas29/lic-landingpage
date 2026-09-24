from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'mobile_number', 'email', 'city', 'qualification', 'consent_given']

    def clean_consent_given(self):
        consent = self.cleaned_data.get('consent_given')
        if not consent:
            raise forms.ValidationError("You must consent to be contacted to submit this application.")
        return consent

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number', '')
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return mobile_number
