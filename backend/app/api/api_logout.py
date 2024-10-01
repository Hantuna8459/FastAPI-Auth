from fastapi import APIRouter, Depends, HTTPException, Response

router = APIRouter()

@router.post("/logout")
def logout(response:Response):
    return None