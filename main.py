from fastapi import FastAPI , HTTPException , status ,  Response
from fastapi.middleware.cors import CORSMiddleware
import json
#App object
app = FastAPI()
from model import Todo , User , NewUser
from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)
origins = ['http://localhost:3000','http://localhost:8000','http://localhost:8000/api/todo','https://farmstack-frontend.onrender.com/']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    expose_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return {"Ping":"Pong"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


@app.get("/api/todo/{title}" , response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(status_code=404,detail=f"There is no TODO item with this title {title}")

@app.post("/api/todo")
async def post_todo(todo:Todo,response:Response)->Todo:
    todo=todo.dict()
    title=todo["title"]
    resp=await fetch_one_todo(title)
    if resp:
        raise HTTPException(status_code=403,detail="You are not allowed to add a document with the given title as it is already there.Try update instead.")
    result = await create_todo(todo)
    if result:
        response.status_code=status.HTTP_201_CREATED
        return result
    

@app.put("/api/todo/" , response_model=Todo)
async def put_todo(todo:Todo,response : Response):
    todo=todo.dict()
    result=await update_todo(todo["title"],todo["description"])
    return result
    

@app.delete("/api/todo/{title}" , response_model=Todo)
async def delete_todo(title,response : Response):
    result = await remove_todo(title)
    if result:
        response.status_code=status.HTTP_204_NO_CONTENT
        return {
                "title": "Status",
                "description": "Successfully deleted todo item !"
               }
    else:
        raise HTTPException(status_code=404,detail=f"There is no TODO item with this title {title}")

#Simple authentication code continues from here


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/sign_up")
def sign_up(new_user:NewUser):
    try:
        user= json.loads(User.objects.get(username=new_user.username).to_json())
        raise HTTPException(status_code=403,detail="User already exists")
    except User.DoesNotExist:
        user=User(username=new_user.username,
                password=get_password_hash(new_user.password))
        user.save()
        return {"message":"New user created successfully"}

from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from fastapi import Depends
from datetime import datetime
from datetime import timedelta
from jose import jwt
SECRET_KEY = 'bd064bfbdbfb077576a3f687eff9fb94cbd1b1c113feb0c7440d7587abedf2f1'
ALGORITHM ='HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username,password):
    try:
        user= json.loads(User.objects.get(username=username).to_json())
        password_check=pwd_context.verify(password,user['password'])
        return password_check
    except User.DoesNotExist:
        return False
    

def create_access_token(data:dict,expires_delta:timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow()+expires_delta
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
def login(form_data:OAuth2PasswordRequestForm = Depends()):
    username=form_data.username
    password=form_data.password
    if authenticate_user(username,password):
        access_token=create_access_token(
            data={"sub":username},expires_delta=timedelta(minutes=30)
        )
        return {"access_token":access_token,"token_type":"bearer"}
    else :
        raise HTTPException(status_code=400,detail="Incorrect username or password")
    print(username,password)


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")

@app.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}

@app.get("/")
def home(token: str = Depends(oauth2_scheme)):
    return {"token":token}

