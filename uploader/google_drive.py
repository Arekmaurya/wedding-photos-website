import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
import io

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRET_FILE = 'client_secret.json'
TOKEN_FILE = 'token.json'

import json

def get_drive_service():
    # Define potential paths for secret files (Render puts them in /etc/secrets/)
    RENDER_TOKEN_PATH = '/etc/secrets/token.json'
    RENDER_CLIENT_SECRET_PATH = '/etc/secrets/client_secret.json'
    
    token_file = RENDER_TOKEN_PATH if os.path.exists(RENDER_TOKEN_PATH) else TOKEN_FILE
    client_secret_file = RENDER_CLIENT_SECRET_PATH if os.path.exists(RENDER_CLIENT_SECRET_PATH) else CLIENT_SECRET_FILE

    creds = None
    # 1. Try to load from environment variable (for Render/Production)
    env_token = os.environ.get('GOOGLE_DRIVE_TOKEN')
    if env_token:
        try:
            token_data = json.loads(env_token)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"Error loading token from environment: {e}")

    # 2. Try to load from file (Local or Render Secret File)
    if not creds and os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception as e:
            print(f"Error loading token from file {token_file}: {e}")
        
    # 3. If still no valid creds, trigger the browser flow (Only works on Desktop)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing Google Drive credentials...")
            creds.refresh(Request())
        else:
            print("No valid credentials found. Starting local auth flow...")
            # Re-read client secret from correct path
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Update local token file only if it's not a read-only secret path
        if not token_file.startswith('/etc/secrets/'):
            try:
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
                print(f"Updated local token file: {token_file}")
            except Exception as e:
                print(f"Failed to update token file: {e}")
            
    return build('drive', 'v3', credentials=creds)

def get_or_create_folder(service, folder_name, parent_id=None):
    """Check if folder exists, if not create it and return folder ID"""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
        
    results = service.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)', supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    items = results.get('files', [])
    
    if items:
        return items[0].get('id')
    
    # Create the folder
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        folder_metadata['parents'] = [parent_id]
        
    folder = service.files().create(body=folder_metadata, fields='id', supportsAllDrives=True).execute()
    return folder.get('id')

def upload_files(guest_name, files, message=None):
    """Upload list of files to a specific folder named after the guest."""
    service = get_drive_service()
    
    # Optional: If you want a root "Wedding Uploads" folder, specify its ID here.
    wedding_root_folder_id = '1o8gaoOc8nOKuFGt0Ne5YycsP_2whQfsw' 
    
    # Create a unique folder for THIS upload session/guest
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{guest_name}_{timestamp}"
    
    # Get or create a specific folder for this guest inside the Wedding root folder
    guest_folder_id = get_or_create_folder(service, folder_name, parent_id=wedding_root_folder_id)
    
    # 1. Upload the guest message if it exists
    if message and message.strip():
        file_metadata = {
            'name': 'message.txt',
            'parents': [guest_folder_id]
        }
        fh = io.BytesIO(message.encode('utf-8'))
        media = MediaIoBaseUpload(fh, mimetype='text/plain', resumable=True)
        
        try:
            msg_file = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
            print(f"Message saved with ID: {msg_file.get('id')}", flush=True)
        except Exception as e:
            print(f"Error saving message: {e}", flush=True)

    # 2. Upload each file to that folder
    import gc
    for file in files:
        file_metadata = {
            'name': file.name,
            'parents': [guest_folder_id]
        }
        
        # Explicitly set a very small chunk size (1MB) to prevent RAM spikes on Render
        media = MediaIoBaseUpload(file.file, mimetype=file.content_type, resumable=True, chunksize=1024*1024)
        
        request = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}% of {file.name}.")
        print(f"File ID: {response.get('id')} uploaded successfully.")
        
        # Force memory cleanup after each file is finished
        gc.collect()

def list_all_uploads():
    """Fetches all folders and their files from the Wedding Uploads directory."""
    service = get_drive_service()
    wedding_root_folder_id = '1o8gaoOc8nOKuFGt0Ne5YycsP_2whQfsw'
    
    # 1. List all folders (each folder is one guest upload session)
    query = f"'{wedding_root_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(
        q=query, 
        fields='files(id, name, createdTime)', 
        orderBy='createdTime desc',
        supportsAllDrives=True, 
        includeItemsFromAllDrives=True
    ).execute()
    folders = results.get('files', [])
    
    gallery_data = []
    
    # 2. For each folder, get its files
    for folder in folders:
        folder_id = folder['id']
        file_query = f"'{folder_id}' in parents and trashed=false"
        file_results = service.files().list(
            q=file_query, 
            fields='files(id, name, mimeType, webViewLink, thumbnailLink)',
            supportsAllDrives=True, 
            includeItemsFromAllDrives=True
        ).execute()
        files = file_results.get('files', [])
        
        # Look for the message.txt if it exists
        message = ""
        media_files = []
        for f in files:
            if f['name'] == 'message.txt':
                # Fetch content of message.txt
                try:
                    request = service.files().get_media(fileId=f['id'])
                    message = request.execute().decode('utf-8')
                except:
                    message = "Could not load message."
            elif 'image' in f['mimeType'] or 'video' in f['mimeType']:
                media_files.append(f)
        
        gallery_data.append({
            'folder_name': folder['name'],
            'created_at': folder['createdTime'],
            'message': message,
            'files': media_files
        })
        
    return gallery_data
