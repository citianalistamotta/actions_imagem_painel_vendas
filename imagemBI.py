import os
import requests
from datetime import datetime
from pdf2image import convert_from_path
from google_drive_uploader import GoogleDriveUploader

class ImagemBI:
    def __init__(self):
        # Credenciais Power BI via GitHub Secrets (limpando espaços e quebras de linha)
        self.CLIENT_ID = os.environ["POWERBI_CLIENT_ID"].strip()
        self.TENANT_ID = os.environ["POWERBI_TENANT_ID"].strip()
        self.CLIENT_SECRET = os.environ["POWERBI_CLIENT_SECRET"].strip()
        self.WORKSPACE_ID = os.environ["POWERBI_WORKSPACE_ID"].strip()
        self.REPORT_ID = os.environ["POWERBI_REPORT_ID"].strip()

        # Debug seguro
        print("Tenant ID length:", len(self.TENANT_ID))

        # Google Drive
        self.CREDENCIAIS_JSON = "json_servico.json"  # caminho do seu JSON
        self.DRIVE_FOLDER_ID = "0AIKhHd2CLvXxUk9PVA"

        # Pasta local
        os.makedirs("reports", exist_ok=True)

    def get_access_token(self):
        url = f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "scope": "https://analysis.windows.net/powerbi/api/.default"
        }
        r = requests.post(url, data=payload)
        r.raise_for_status()
        return r.json()["access_token"]

    def export_report_pdf(self):
        token = self.get_access_token()
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.WORKSPACE_ID}/reports/{self.REPORT_ID}/ExportTo"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {"format": "PDF"}
        r = requests.post(url, headers=headers, json=payload)
        r.raise_for_status()

        data_hoje = datetime.now().strftime("%Y-%m-%d")
        pdf_path = os.path.join("reports", f"painel_{data_hoje}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(r.content)

        print(f"PDF salvo: {pdf_path}")
        return pdf_path

    def pdf_to_jpeg(self, pdf_path):
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        images = convert_from_path(pdf_path, dpi=200)
        jpeg_paths = []

        for i, page in enumerate(images):
            jpeg_path = os.path.join("reports", f"painel_{data_hoje}_page{i+1}.jpeg")
            page.save(jpeg_path, "JPEG")
            jpeg_paths.append(jpeg_path)
            print(f"JPEG salvo: {jpeg_path}")

        return jpeg_paths

    def upload_to_drive(self, file_paths):
        uploader = GoogleDriveUploader(self.CREDENCIAIS_JSON, self.DRIVE_FOLDER_ID)
        links = []
        for path in file_paths:
            link = uploader.upload_file(path, os.path.basename(path))
            print(f"Arquivo enviado: {link}")
            links.append(link)
        return links

    def capturar_e_enviar(self):
        pdf_path = self.export_report_pdf()
        jpeg_paths = self.pdf_to_jpeg(pdf_path)
        links = self.upload_to_drive(jpeg_paths)
        return links

    def get_access_token(self):
        print("CLIENT_ID:", self.CLIENT_ID)
        print("TENANT_ID:", self.TENANT_ID)
        print("CLIENT_SECRET:", self.CLIENT_SECRET)
