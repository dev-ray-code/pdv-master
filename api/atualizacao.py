"""
Endpoint de atualização automática do PDV.

O PDV cliente consulta GET /atualizacao/versao ao abrir.
Se a versão disponível for maior que a local, o cliente
avisa o usuário e oferece o botão "Atualizar agora".

COMO PUBLICAR UMA NOVA VERSÃO:
1. Gere o novo PDV Store.exe com o PyInstaller
2. Suba o .exe para algum lugar de download direto
   (GitHub Releases, Google Drive com link direto, S3, etc.)
3. Atualize as variáveis de ambiente no Render:
     PDV_VERSAO_ATUAL  → ex: "1.2.0"
     PDV_URL_DOWNLOAD  → URL direta do novo .exe
4. Faça o deploy — o PDV de todos os clientes vai perceber
   a nova versão no próximo login e avisar automaticamente.

Sobre onde hospedar o .exe:
- GitHub Releases é a opção mais simples e gratuita.
  Crie um release em github.com/dev-ray-code/pdv-master/releases
  e copie o link direto do arquivo .exe.
- O link precisa ser direto (forçar download), não uma página HTML.
"""

import os
from fastapi import APIRouter

router = APIRouter(
    prefix="/atualizacao",
    tags=["Atualização"]
)

# Versão atual disponível para download.
# Defina no Render: PDV_VERSAO_ATUAL = "1.0.0"
# Quando quiser publicar uma versão nova, mude para "1.1.0" (ou o que for)
# e atualize também o PDV_URL_DOWNLOAD.
PDV_VERSAO_ATUAL = os.getenv("PDV_VERSAO_ATUAL", "1.0.0")

# URL direta do .exe para download.
# Defina no Render: PDV_URL_DOWNLOAD = "https://..."
# Enquanto não estiver configurada, retorna string vazia e o
# cliente não vai oferecer atualização (comportamento seguro).
PDV_URL_DOWNLOAD = os.getenv("PDV_URL_DOWNLOAD", "")


@router.get("/versao")
def versao_disponivel():
    """
    Consultado pelo PDV cliente em background ao abrir.
    Retorna a versão mais recente disponível e a URL de download.
    Rota pública — não precisa de token (o PDV consulta antes do login).
    """
    return {
        "versao": PDV_VERSAO_ATUAL,
        "url_download": PDV_URL_DOWNLOAD,
        "obrigatorio": False   # True = o cliente não abre sem atualizar (reservado para o futuro)
    }