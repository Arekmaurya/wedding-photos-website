# Wedding Upload App: Next Steps

We successfully built the Django app, linked the Google Drive API, and created the `client_secret.json` OAuth file. 

The very last step before the app is fully functional is to test it, which requires adding you as a "Test user" in Google Cloud.

## Where We Left Off
When you run the test upload script, Google blocks the sign-in because your email address is not whitelisted in the Google Cloud Console. Since the app is in "Testing" mode, Google explicitly requires this.

## How to Resume Later
When you are ready to finish the setup, follow these steps:

**1. Whitelist your email:**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and ensure you have the `My First Project` (or the project you used) selected.
2. In the search bar at the top, type **"Google Auth Platform"** and click on it.
3. On the left-hand menu, click **Audience**.
4. Scroll down right to the bottom to the **Test users** section.
5. Click the **+ Add Users** button.
6. Type exactly your email address: `harshmaurya82500@gmail.com`
7. Click **Add / Save**.

**2. Run the final test:**
Now that your email is explicitly allowed to use the app, we need to generate the local `token.json` file.

1. Open PowerShell or Command Prompt.
2. Run these commands:
   ```cmd
   cd OneDrive\Desktop\wedding
   .\venv\Scripts\activate
   python test_upload.py
   ```
3. A Google Sign-in screen will pop up. Sign in with `harshmaurya82500@gmail.com`.
4. If you see a warning screen saying "Google hasn't verified this app", click **Advanced** at the bottom, then click **Go to Wedding Uploader (unsafe)**.
5. Check all the boxes to allow the app to access your Google Drive and click **Continue**.

The terminal will print **"Direct upload test passed!"**, and a `token.json` file will appear in your folder. 

Once that file exists, the actual Django web app will work perfectly, and you can run `python manage.py runserver` to use the website!
