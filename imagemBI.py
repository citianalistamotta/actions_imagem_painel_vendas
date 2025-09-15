import os
import io
import time
from datetime import datetime
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from google_drive_uploader import GoogleDriveUploader

class ImagemBI:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Configurações Google Drive
        self.CREDENCIAIS_JSON = os.path.join(self.BASE_DIR, "json_servico.json")
        self.DRIVE_FOLDER_ID = "0AIKhHd2CLvXxUk9PVA" 

        # Configurações Power BI
        self.EMAIL = "mateus@motta.com.br"
        self.SENHA = "PlanInt2025$"

    def capturar_painel_powerbi(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://login.microsoftonline.com/")

        try:
            wait = WebDriverWait(driver, 30)

            # Login
            time.sleep(5)
            input_email = wait.until(EC.presence_of_element_located((By.NAME, "loginfmt")))
            input_email.send_keys(self.EMAIL)
            driver.find_element(By.ID, "idSIButton9").click()

            time.sleep(5)
            input_senha = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
            input_senha.send_keys(self.SENHA)
            driver.find_element(By.ID, "idSIButton9").click()

            try:
                time.sleep(5)
                botao_sim = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
                botao_sim.click()
            except:
                pass

            # Abrir painel
            time.sleep(10)
            driver.get("https://app.fabric.microsoft.com/groups/87eb8147-a8e1-4f35-b2b1-517e534bb6c2/reports/30136b4d-75ae-44af-a192-ac42a25fb8f1/ReportSection85edb67b7778d4ac3aee?experience=fabric-developer&chromeless=true&navContentPaneEnabled=false&filterPaneEnabled=false")
            time.sleep(15)

            try:
                aviso_avaliacao = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="content"]/tri-shell/tri-item-renderer/tri-extension-page-outlet/div[2]/report/exploration-container/div/div/docking-container/div/div/div/notification-bar/div/div[2]/button[2]')))
                aviso_avaliacao.click()
            except:
                print("Aviso de avaliação gratuita não encontrado ou já fechado.")
            time.sleep(1)

            painel_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]')))

            png = painel_element.screenshot_as_png

            # Salvar local
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            pasta_destino = os.path.join("reports", "reportsoutput")
            os.makedirs(pasta_destino, exist_ok=True)
            caminho_jpeg = os.path.join(pasta_destino, f"painel_{data_hoje}.jpeg")
            img = Image.open(io.BytesIO(png)).convert("RGB")
            img.save(caminho_jpeg, "JPEG")
            print(f"Imagem salva: {caminho_jpeg}")

            # Upload Google Drive
            uploader = GoogleDriveUploader(self.CREDENCIAIS_JSON, self.DRIVE_FOLDER_ID)
            link_publico = uploader.upload_file(caminho_jpeg, f"painel_{data_hoje}.jpeg")
            return link_publico

        except Exception as e:
            print(f"❌ Erro durante captura/upload: {e}")
            return None
        finally:
            driver.quit()