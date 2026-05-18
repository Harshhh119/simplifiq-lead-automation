from googleapiclient.discovery import build
import google.oauth2.service_account
from httplib2 import Credentials
from app.config import settings
from datetime import datetime
import os
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def get_google_creds():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        return None
    try:
        # If the file reads empty or has placeholders, fail gracefully
        return Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    except Exception:
        return None

async def log_lead_to_sheets(name: str, email: str, company: str, status: str):
    creds = get_google_creds()
    if not creds or not settings.GOOGLE_SHEET_ID: return
    try:
        service = build('sheets', 'v4', credentials=creds)
        values = [[name, email, company, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), status]]
        service.spreadsheets().values().append(
            spreadsheetId=settings.GOOGLE_SHEET_ID, range="Sheet1!A:E",
            valueInputOption="USER_ENTERED", body={'values': values}
        ).execute()
    except Exception as e: print(f"Sheets error: {e}")

async def archive_pdf_to_drive(file_path: str, company_name: str) -> str:
    creds = get_google_creds()
    if not creds or not settings.GOOGLE_DRIVE_FOLDER_ID: return ""
    try:
        service = build('drive', 'v3', credentials=creds)
        meta = {
            'name': f"SimplifIQ_{company_name}_Report_{datetime.utcnow().strftime('%Y%m%d')}.pdf",
            'parents': [settings.GOOGLE_DRIVE_FOLDER_ID]
        }
        from googleapiclient.http import MediaFileUpload
        media = MediaFileUpload(file_path, mimetype='application/pdf')
        file = service.files().create(body=meta, media_body=media, fields='id').execute()
        return file.get('id')
    except Exception as e:
        print(f"Drive error: {e}")
        return ""