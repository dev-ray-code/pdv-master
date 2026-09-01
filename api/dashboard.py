from fastapi import APIRouter, Depends

from api.admin_auth import verificar_admin_token

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(verificar_admin_token)]
)

@router.get("/")
def dashboard():
    return {
        "status": "ok",
        "mensagem": "Dashboard funcionando."
    }