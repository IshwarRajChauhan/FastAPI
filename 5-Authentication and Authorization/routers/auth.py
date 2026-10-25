from datetime import datetime, timedelta, timezone     #handling token expiration
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import users        #database table from madels.py
from database import SessionLocal
from passlib.context import CryptContext        # for password hashing
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer   
# OAuth2PasswordRequestForm	: Reads username and password submitted as form data
# OAuth2PasswordBearer : Extracts a bearer token from the Authorization header
from jose import jwt,JWTError  #JWT creation and verification

# What each group does:
# - datetime, timedelta, timezone — calculate JWT expiration.
# - Annotated — define reusable dependency types.
# - APIRouter, Depends, HTTPException, status — routes, dependency injection, and HTTP errors.
# - BaseModel — validate request and response data.
# - Session — database interaction.
# - User — your SQLAlchemy user model.
# - SessionLocal — create database sessions.
# - CryptContext — hash and verify passwords.
# - OAuth2PasswordRequestForm — read login credentials.
# - OAuth2PasswordBearer — extract the bearer token.
# - jwt, JWTError — create and validate JWTs. 


# -------------------------------------------------------------------


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

#Why? This groups your authentication endpoints under /auth
# -------------------------------------------------------------------

SECRET_KEY = '38695eb2ae0cef08fb8272fd0439450d282276c729f5169e083f348ea9304829'
ALGORITHM = 'HS256'


bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')      #password hashing
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')              #extracting the JWT

# SECRET_KEY and ALGORITHM configure JWT signing and verification.
# bcrypt_context handles password hashing.
# oauth2_bearer extracts a JWT from the request's Authorization header.

# -------------------------------------------------------------------

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str



class Token(BaseModel):
    access_token : str
    token_type : str

# -------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Database dependy for user table

# -------------------------------------------------------------------


def authenticate_user(username:str,password:str,db):
    user = db.query(users).filter(users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user


# If authentication fails, the endpoint rejects the login. 
# If it succeeds, the endpoint creates a JWT.

# -------------------------------------------------------------------

def create_access_token(username: str,user_id:int,expires_delta: timedelta):
    encode = {'sub':username,'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


# sub — identifies the subject, which is the username here.
# id — stores your user's database ID.

# -------------------------------------------------------------------


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not Validate User.')
        return {"Username": username , "ID": user_id}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not Validate User.')


# -------------------------------------------------------------------





@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:CreateUserRequest):
    create_user_model = users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )
    
    db.add(create_user_model)
    db.commit()

# -------------------------------------------------------------------




@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not Validate User.')

    token = create_access_token(user.username,user.id,timedelta(minutes=20))
    return {"access_token":token,'token_type':'bearer'}
    
    















