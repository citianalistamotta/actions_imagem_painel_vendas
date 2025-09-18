from datetime import datetime
from imagemBI import ImagemBI
from relatorio_api import RelatorioAPI

if __name__ == "__main__":
    data_atual = datetime.now()
    imagem = ImagemBI()
    relatorio_api = RelatorioAPI()

    imagem.get_access_token()  # Verifica se o token está sendo obtido corretamente

    print("----------------------------- Captura Painel -----------------------")
    links = imagem.capturar_e_enviar()
    print("Links dos arquivos no Google Drive:", links)

    print("----------------------------- Envio via API -----------------------")
    relatorio_api.enviar_relatorio_servicos(links)