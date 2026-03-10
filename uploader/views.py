from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .google_drive import upload_files

def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            guest_name = form.cleaned_data['guest_name']
            
            if not files:
            guest_name = form.cleaned_data['guest_name']
            
            if not files:
                print("MANUAL VALIDATION: No files found in request.FILES", flush=True)
                return render(request, 'uploader/upload.html', {
                    'form': form, 
                    'error_message': 'Please select at least one photo or video to upload.'
                })

            print(f"Files received for {guest_name}: {[f.name for f in files]}", flush=True)
            
            try:
                # Send the files and guest_name to Google Drive
                upload_files(guest_name, files)
            except Exception as e:
                print(f"UPLOAD ERROR: {e}", flush=True)
                return render(request, 'uploader/upload.html', {
                    'form': form, 
                    'error_message': f'Drive Error: {str(e)}'
                })
            
            return render(request, 'uploader/success.html', {'guest_name': guest_name})
        else:
            print(f"FORM INVALID: {form.errors}", flush=True)
    else:
        form = UploadFileForm()
    return render(request, 'uploader/upload.html', {'form': form})
