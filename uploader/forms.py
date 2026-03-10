from django import forms

class UploadFileForm(forms.Form):
    guest_name = forms.CharField(max_length=100, label="Your Name", required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a sweet note for the couple...'}), required=False, label="Leave a Message")
