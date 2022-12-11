from fastapi import APIRouter,HTTPException, status,Depends, Request
from app.model.users import UsersModel
from app.database.connection import get_db
from sqlalchemy.orm import Session
from app.schema.users import Users,Login,ForgotPassword
from app.helper.hash import create_hash
from app.helper.email import simple_send
from app.helper.auth import very_token
import jwt
import time
from pathlib import Path
from fastapi.templating import Jinja2Templates

user_router= APIRouter()


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_registration(create_user:Users, db:Session =Depends(get_db)):
    user_exist =db.query(UsersModel).filter(UsersModel.email == create_user.email).first()
    if user_exist:
       raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                           detail=f"User with email provided exists already.")
    new_user = UsersModel(**create_user.dict())
    new_user.password = create_hash(create_user.password)
    await simple_send(new_user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
       "status":"successful",
       "message":"Please check your Email Address for Verification"
       }

@user_router.get("/verification")
async def verification(request:Request, token: str):
    user = await very_token(token)
    return user

@user_router.post('/login',status_code=status.HTTP_200_OK)
def login_user(user_login:Login ,db:Session =Depends(get_db)):
    user_exist = db.query(UsersModel).filter(UsersModel.email == user_login.email).first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with email and password does not exist."
                            )
    
    # user_password=db.query(UsersModel).filter(UsersModel.password ==user_login.password).first()
    # if not user_password:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail="User with email and password does not exist."
                            # )
    if user_exist.is_verified != False :
        payload ={
            "id":user_exist.id,
            "email":user_exist.email,
            "expires":time.time() + 600
        }
        secret="14631206e9daa6aa9f470bebf55bb5d3"
        algorithm='HS256'
        accestoken=jwt.encode(payload,secret,algorithm=algorithm)
        return {
            "status":"login successful",
            "accesstoken":accestoken
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Please verify your account, Thanks "
                            )


Base_Dir=Path(__file__).resolve().parent
template =Jinja2Templates(directory=str(Path(Base_Dir,'templates/')))        
@user_router.post('/forgot_password',status_code=status.HTTP_200_OK)

def forgotPassword(user_email:ForgotPassword,db:Session = Depends(get_db)):
    email_exits =db.query(UsersModel).filter(UsersModel.email ==user_email.email).first()
    if email_exits:
        return 
    else:
        return {"message":"email not sent"}
        
        
@user_router.get("/current_user")
async def get_current_user():
    # secret="14631206e9daa6aa9f470bebf55bb5d3"
    # algorithm='HS256'
    # payload = await jwt.decode(token,secret,algorithms=algorithm)
    # response = payload.get('email')
    return 