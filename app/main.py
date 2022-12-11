from fastapi import FastAPI,Request
from app.model import users,project
from app.service.users import user_router
from app.database.connection import engine
from fastapi.templating import Jinja2Templates
from pathlib import Path
from dotenv import dotenv_values




config_credentials = dotenv_values(".env")




app = FastAPI()


users.Base.metadata.create_all(bind=engine)


Base_DIR = Path(__file__).resolve().parent
config_credentials = dotenv_values(".env")








templates=Jinja2Templates(directory=str(Path(Base_DIR,'templates/')))
@app.get("/")
def run_move(request:Request):
    return templates.TemplateResponse("forgot_password.html",{"request": request})

       
    
app.include_router(user_router,prefix='/user')