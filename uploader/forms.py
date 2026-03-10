from django import forms

class UploadFileForm(forms.Form):
    guest_name = forms.CharField(max_length=100, label="Your Name", required=True)
