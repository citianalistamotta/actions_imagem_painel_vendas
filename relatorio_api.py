import requests
from datetime import datetime

class RelatorioAPI:
    def __init__(self):
        self.token = "35B9B8575417BA1E06A63914"
        self.id_instancia = "3E7478A3D69FB1B33F60A6F61CAAA8C7"
        self.contatos = {"Samantha": "+5567992905861"}
        self.url_base = f'https://api.z-api.io/instances/{self.id_instancia}/token/{self.token}'
        self.headers = {
            "Content-Type": "application/json",
            "Client-Token": "F0e909a12f87c4194b48dbb02048b05fdS"
        }

    def enviar_imagem(self, telefone: str, imagem_url: str, caption: str = ''):
        url = f'{self.url_base}/send-image'
        payload = {
            "phone": telefone,
            "image": imagem_url,
            "caption": caption
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response_json = response.json()
        except Exception as e:
            print(f"❌ Erro na requisição para {telefone}: {e}")
            return

        if response.status_code == 200 and not response_json.get('error'):
            print(f"✅ Imagem enviada com sucesso para {telefone}")
        else:
            print(f"❌ Falha ao enviar imagem para {telefone}: {response.status_code} - {response_json}")

    def enviar_relatorio_servicos(self, imagem_url: str):
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        legenda = f"Relatório do dia {data_hoje}"

        if not imagem_url:
            print("❌ Nenhuma URL de imagem fornecida.")
            return

        for nome, numero in self.contatos.items():
            print(f"Enviando relatório para {nome} ({numero})...")
            self.enviar_imagem(numero, imagem_url, caption=legenda)
