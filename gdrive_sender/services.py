from io import BytesIO

from django.conf import settings
from google.auth.exceptions import GoogleAuthError
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from .excepitons import GoogleDriveServiceError


class GoogleDriveService:
    def __init__(self):
        try:
            self.credentials = Credentials.from_service_account_file(
                settings.GOOGLE_SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/drive"],
            )
            self.service = build("drive", "v3", credentials=self.credentials)
        except (GoogleAuthError, FileNotFoundError) as e:
            raise GoogleDriveServiceError(f"Error initializing GoogleDriveService")

    def file_exists(self, file_name):
        try:
            existing_files = (
                self.service.files().list(q=f"name='{file_name}'").execute()
            )
            return bool(existing_files.get("files"))
        except HttpError as e:
            raise GoogleDriveServiceError(f"Error checking if file exists")

    def create_file(self, file_name: str, text_content: str):
        try:
            file_content = BytesIO(text_content.encode("utf-8"))

            file_metadata = {"name": file_name}
            media = MediaIoBaseUpload(
                file_content, mimetype="text/plain", resumable=True
            )
            file = (
                self.service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            return file.get("id")
        except HttpError as e:
            raise GoogleDriveServiceError(f"Error creating file")
