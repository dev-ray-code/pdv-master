from fastapi import APIRouter

router = APIRouter(
    prefix="/mobile",
    tags=["Mobile"]
)

@router.get("/")
def mobile():
    return {
        "status": "ok",
        "mensagem": "Mobile funcionando."
    }