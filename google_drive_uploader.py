from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class GoogleDriveUploader:
    def __init__(self, credentials_json_path, shared_drive_id):
        """
        credentials_json_path: caminho para o JSON do Service Account
        shared_drive_id: ID do Shared Drive onde os arquivos serão enviados
        """
        self.shared_drive_id = shared_drive_id
        self.creds = service_account.Credentials.from_service_account_file(credentials_json_path)
        self.service = build('drive', 'v3', credentials=self.creds)

    def upload_file(self, file_path, file_name):
        """
        Faz upload do arquivo para o Shared Drive e retorna a URL pública.
        """
        # Metadados do arquivo
        file_metadata = {
            'name': file_name,
            'parents': [self.shared_drive_id]
        }

        media = MediaFileUpload(file_path, resumable=True)

        # Upload no Shared Drive
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        ).execute()

        file_id = file['id']
        print(f" Arquivo enviado para o Shared Drive. File ID: {file_id}")

        # Tornar público para gerar link
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        self.service.permissions().create(
            fileId=file_id,
            body=permission,
            supportsAllDrives=True
        ).execute()

        public_url = f"https:/drive.google.com/uc?id={file_id}"
        print(f" URL pública: {public_url}")

        return public_url