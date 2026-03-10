from django import forms

class UploadFileForm(forms.Form):
    guest_name = forms.CharField(max_length=100, label="Your Name", required=True)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Select Photos & Videos')
