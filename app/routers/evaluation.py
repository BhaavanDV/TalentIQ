from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_evaluations():
    return {"message": "List of evaluations"}