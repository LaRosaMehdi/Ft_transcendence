from django import forms

class TwoFactorForm(forms.Form):
    validation_code = forms.CharField(label='Validation Code', max_length=6, min_length=6)

    def clean_validation_code(self):
        validation_code = self.cleaned_data['validation_code']
        if not validation_code.isdigit() or len(validation_code) != 6:
            raise forms.ValidationError("Please enter a valid 6-digit code.")
        return validation_code