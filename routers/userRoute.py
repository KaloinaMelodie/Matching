from fastapi import APIRouter
import controllers.userController as userCtrl

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users():
    return userCtrl.helloUser()

