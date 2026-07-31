from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def dashboard():
    return {
        "status": "ok",
        "mensagem": "Dashboard funcionando."
    }