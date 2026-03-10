# Wedding Memory Envelope 🕊️📸

A beautiful, modern Django web application for guests to upload photos and videos directly to a private Google Drive folder. Perfect for weddings and special events!

## ✨ Features

- **🚀 Real-Time Progress Bar:** Visual feedback for large file uploads.
- **📱 Mobile Friendly:** Clean, elegant design that works on any device.
- **✍️ Guest Messages:** Guests can leave a sweet note along with their media.
- **📁 Smart Organization:** Each upload session is organized into its own folder on Google Drive.
- **🎨 Premium Aesthetics:** Features a sophisticated, wedding-themed UI with smooth animations.
- **🖼️ Private Admin Gallery:** A secure dashboard to browse and view all uploaded memories in a grid.

## 🛠️ Tech Stack

- **Backend:** Django (Python 3.11+)
- **Storage:** Google Drive API v3
- **Frontend:** Vanilla JS, AJAX, and elegant CSS (Inter & Playfair Display fonts)
- **Deployment:** Optimized for Render (Gunicorn & Whitenoise)

## 🚀 Quick Setup (Render Deployment)

1. **Google Cloud Console:**
   - Create a project and enable the **Google Drive API**.
   - Create an **OAuth 2.0 Client ID** (Desktop app type).
   - Download the `client_secret.json` and keep it in the root folder.
   - Run the app locally once to generate `token.json` via the browser.

2. **Render Configuration:**
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn wedding_project.wsgi`
   - **Environment Variables:**
     - `GOOGLE_DRIVE_TOKEN`: (Paste the entire contents of your `token.json`)
     - `SECRET_KEY`: (Your Django secret key)
     - `ADMIN_PASSWORD`: (Password for the `/gallery/` page)
     - `RENDER`: `True`

3. **Visit your site:**
   - Upload memories at `/`
   - View the gallery at `/gallery/`

## 🔒 Security

- **Private Gallery:** Protected by a simple password check.
- **Headless Auth:** Uses environment variables for Google Drive tokens, making it safe for cloud deployment.
- **Large File Handling:** Supports uploads up to 500MB per batch by default.

---
*Created for Himanshu & Namrata's Special Day 🕊️*
