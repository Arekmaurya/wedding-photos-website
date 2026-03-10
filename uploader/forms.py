from django import forms

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class UploadFileForm(forms.Form):
    guest_name = forms.CharField(max_length=100, label="Your Name", required=True)
    file = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}), 
        label='Select Photos & Videos',
        required=False  # Handled manually in view
    )
