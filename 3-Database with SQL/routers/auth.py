from fastapi import APIRouter
from pydantic import BaseModel
from models import users
from passlib.context import CryptContext



#To use different fastapi app , we need to route it 
# 1.First create a routers folder , and in it create your file
# 2. Import APIRouters , and just we create an instance of app , we create an instance of router
# 3.Now use that instance in place of app



router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth")
async def create_user(create_user_request:CreateUserRequest):
    create_user_model = users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )
    return create_user_model



















