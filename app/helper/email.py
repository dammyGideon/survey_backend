from fastapi import (BackgroundTasks,UploadFile,File,Form,Depends,HTTPException,status)
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.model.users import UsersModel
from dotenv import dotenv_values
import jwt
config_credentials = dotenv_values(".env")


conf = ConnectionConfig(
    MAIL_USERNAME = "439fcec5f7d974",
    MAIL_PASSWORD = "18a0e177bd77b8",
    MAIL_FROM = "test@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.mailtrap.io",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def simple_send(email:EmailStr):
    token_data ={
            "email":email,
        }
    secret="14631206e9daa6aa9f470bebf55bb5d3"
    token = jwt.encode(token_data,secret, algorithm='HS256')
    
    template = f"""
            <!DOCTYPE html>
            <html>
                <head> </head> 
                <body>
                    <div style="display: flex; align-items:center; justify-content:center; flex-direction:column">
                    <h3>Account Verification </h3>
                    <br>
                    
                    <p>Thanks for choosing Survey, please click on the button below to verify your account</p>
                    <a href="http://localhost:8000/verification/?token={token}">Verify Your Account</a>
                    <p>
                        Please kindly ignore this email if you did not register for Survey and nothing will happend. Thanks 
                    </p>
                </body>
        """
    await message(email,template)
        
async def message(email:str, template):
        message = MessageSchema(
        subject="Survey Verification Mail",
        recipients=[email],
        body=template,
        subtype=MessageType.html)

        fm = FastMail(conf)
        await fm.send_message(message)
        return 

