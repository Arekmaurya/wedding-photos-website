from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
# upload_files was removed in favor of sequential uploads
# from .google_drive import upload_files

def upload_view(request):
    # Handle the success redirect from AJAX
    if request.GET.get('success') == '1':
        guest_name = request.GET.get('name', 'Guest')
        return render(request, 'uploader/success.html', {'guest_name': guest_name})

    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # 1. Handle Initiation (Create Folder & Save Message)
        if 'initiate' in request.POST:
            guest_name = request.POST.get('guest_name', 'Anonymous').strip()
            message = request.POST.get('message', '').strip()
            
            from .google_drive import get_drive_service, create_guest_folder, save_guest_message
            service = get_drive_service()
            if not service:
                return JsonResponse({'success': False, 'error': 'Google Drive service unavailable.'}, status=500)
            
            folder_id = create_guest_folder(service, guest_name)
            if message:
                save_guest_message(service, folder_id, message)
            
            return JsonResponse({'success': True, 'folder_id': folder_id})

        # 2. Handle Single File Upload
        folder_id = request.POST.get('folder_id')
        files = request.FILES.getlist('file')
        
        if not folder_id:
            return JsonResponse({'success': False, 'error': 'No upload session found.'}, status=400)
            
        if not files:
            return JsonResponse({'success': False, 'error': 'No file received.'}, status=400)

        from .google_drive import get_drive_service, upload_single_file
        service = get_drive_service()
        try:
            # We treat 'files' as a list but it should be exactly 1 file in this new flow
            file_id = upload_single_file(service, folder_id, files[0])
            return JsonResponse({'success': True, 'file_id': file_id})
        except Exception as e:
            print(f"Upload error: {e}", flush=True)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # Standard GET request
    form = UploadFileForm()
    return render(request, 'uploader/upload.html', {'form': form})

def gallery_view(request):
    """A private page to view all uploaded photos and videos."""
    try:
        import os
        admin_pass = os.environ.get('ADMIN_PASSWORD', 'wedding2026')
        
        # Check authorization
        authorized = request.session.get('admin_authorized', False)
        
        if request.method == 'POST':
            password = request.POST.get('password')
            if password == admin_pass:
                request.session['admin_authorized'] = True
                request.session.modified = True
                authorized = True
            else:
                return render(request, 'uploader/admin_login.html', {'error': 'Incorrect password'})
                
        if not authorized:
            return render(request, 'uploader/admin_login.html')

        from .google_drive import list_all_uploads
        uploads = list_all_uploads()
        return render(request, 'uploader/admin_gallery.html', {'uploads': uploads})

    except Exception as e:
        import traceback
        error_msg = f"CRITICAL GALLERY ERROR: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, flush=True)
        from django.http import HttpResponse
        return HttpResponse(f"<h3>An unexpected error occurred</h3><pre>{error_msg}</pre>", status=500)
