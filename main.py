from datetime import datetime
from imagemBI import ImagemBI
from relatorio_api import RelatorioAPI

if __name__ == "__main__":
    data_atual = datetime.now()
    imagem = ImagemBI()
    relatorio_api = RelatorioAPI()

    print("----------------------------- Captura Painel -----------------------")
    link_imagem = imagem.capturar_painel_powerbi()

    print("----------------------------- Envio via API -----------------------")
    relatorio_api.enviar_relatorio_servicos(link_imagem)
