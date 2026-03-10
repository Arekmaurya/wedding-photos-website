from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
from .google_drive import upload_files

def upload_view(request):
    # Handle the success redirect from AJAX
    if request.GET.get('success') == '1':
        guest_name = request.GET.get('name', 'Guest')
        return render(request, 'uploader/success.html', {'guest_name': guest_name})

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or \
                  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        if form.is_valid():
            guest_name = form.cleaned_data['guest_name']
            message = form.cleaned_data.get('message', '')
            
            if not files:
                error_msg = 'Please select at least one photo or video to upload.'
                if is_ajax:
                    return JsonResponse({'success': False, 'error': error_msg})
                return render(request, 'uploader/upload.html', {
                    'form': form, 
                    'error_message': error_msg
                })

            print(f"Files received for {guest_name}: {[f.name for f in files]}", flush=True)
            
            try:
                # Send the files, guest_name, and message to Google Drive
                upload_files(guest_name, files, message=message)
                
                if is_ajax:
                    return JsonResponse({'success': True})
                return render(request, 'uploader/success.html', {'guest_name': guest_name})
            
            except Exception as e:
                print(f"UPLOAD ERROR: {e}", flush=True)
                error_msg = f'Drive Error: {str(e)}'
                if is_ajax:
                    return JsonResponse({'success': False, 'error': error_msg})
                return render(request, 'uploader/upload.html', {
                    'form': form, 
                    'error_message': error_msg
                })
        else:
            print(f"FORM INVALID: {form.errors}", flush=True)
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Form invalid. Please check your name.'})
    else:
        form = UploadFileForm()
    
    return render(request, 'uploader/upload.html', {'form': form})
