import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_project.settings')
django.setup()

from uploader.google_drive import upload_files

test_file_path = r"c:\Users\harsh\OneDrive\Desktop\wedding\test_photo.jpg"
with open(test_file_path, 'rb') as f:
    file_content = f.read()

# Simulate Django's UploadedFile object
uploaded_file = SimpleUploadedFile(name='test_photo.jpg', content=file_content, content_type='image/jpeg')

print("Starting direct upload test...")
try:
    upload_files("Backend Test Guest", [uploaded_file])
    print("Direct upload test passed!")
except Exception as e:
    print(f"Upload test failed with error: {e}")
