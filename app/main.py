from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from itertools import count
from threading import Lock

from app.exceptions import CustomExceptionA, CustomExceptionB
from app.schemas import User, UserIn, UserOut
from app.database import engine, Base
from app import models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Control Work", version="1.0.0")


db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()

def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


@app.exception_handler(CustomExceptionA)
async def handle_custom_exception_a(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(CustomExceptionB)
async def handle_custom_exception_b(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "detail": exc.errors(),
            "body": exc.body
        }
    )


@app.get("/trigger-a")
def trigger_a(value: int):
  
    if value < 0:
        raise CustomExceptionA(f"Value {value} is negative")
    return {"status": "ok", "value": value}

@app.get("/trigger-b/{item_id}")
def trigger_b(item_id: int):
  
    if item_id == 0:
        raise CustomExceptionB(f"Item with id {item_id} not found")
    return {"status": "ok", "item_id": item_id}

@app.post("/register")
def register(user: User):
    
    return {"message": f"User {user.username} registered successfully", "user": user.model_dump()}


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
   
    user_id = next_user_id()
    db[user_id] = user.model_dump()
    return {"id": user_id, **db[user_id]}

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
  
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
  
    if db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)

@app.get("/")
def root():
    return {"message": "FastAPI Control Work is running", "docs": "/docs"}