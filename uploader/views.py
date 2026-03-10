from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .google_drive import upload_files

def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            guest_name = form.cleaned_data['guest_name']
            files = request.FILES.getlist('file')
            
            # Send the files and guest_name to Google Drive
            upload_files(guest_name, files)
            
            return render(request, 'uploader/success.html', {'guest_name': guest_name})
    else:
        form = UploadFileForm()
    return render(request, 'uploader/upload.html', {'form': form})
