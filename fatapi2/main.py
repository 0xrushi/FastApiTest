# Python Shorts 
# CRUD with FastAPI 
from typing import List 
import databases 
import sqlalchemy 
from fastapi import FastAPI, status 
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel 

DATABASE_URL = "sqlite:///mydb.db" 
database = databases.Database(DATABASE_URL) 
metadata = sqlalchemy.MetaData() 

todos = sqlalchemy.Table( 
  "todos", 
  metadata, 
  sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True), 
  sqlalchemy.Column("text", sqlalchemy.String), 
  sqlalchemy.Column("completed", sqlalchemy.Boolean), 
) 

engine = sqlalchemy.create_engine( 
  DATABASE_URL 
) 
metadata.create_all(engine) 

class TodoIn(BaseModel): 
  text: str 
  completed: bool 

class Todo(BaseModel): 
  id: int 
  text: str 
  completed: bool 

app = FastAPI(title = "[CRUD] REST API with FastAPI - Async EndPoints") 
app.add_middleware( 
  CORSMiddleware, 
  allow_origins=["*"], 
  allow_credentials=True, 
  allow_methods=["*"], 
  allow_headers=["*"], 
) 

@app.on_event("startup") 
async def startup(): 
  await database.connect() 

@app.on_event("shutdown") 
async def shutdown(): 
  await database.disconnect() 

@app.get("/todos/", response_model=List[Todo], status_code = status.HTTP_200_OK) 
async def read_todos(skip: int = 0, take: int = 20): 
  query = todos.select().offset(skip).limit(take) 
  return await database.fetch_all(query) 

@app.get("/todos/{todo_id}/", response_model=Todo, status_code = status.HTTP_200_OK) 
async def read_todos(todo_id: int): 
  query = todos.select().where(todos.c.id == todo_id) 
  return await database.fetch_one(query) 

@app.post("/todos/", response_model=Todo, status_code = status.HTTP_201_CREATED) 
async def create_todo(todo: TodoIn): 
  query = todos.insert().values(text=todo.text, completed=todo.completed) 
  last_record_id = await database.execute(query) 
  return {**todo.dict(), "id": last_record_id} 

@app.put("/todos/{todo_id}/", response_model=Todo, status_code = status.HTTP_200_OK) 
async def update_todo(todo_id: int, payload: TodoIn): 
  query = todos.update().where(todos.c.id == todo_id).values(text=payload.text, completed=payload.completed) 
  await database.execute(query) 
  return {**payload.dict(), "id": todo_id} 

@app.delete("/todos/{todo_id}/", status_code = status.HTTP_200_OK) 
async def delete_todo(todo_id: int): 
  query = todos.delete().where(todos.c.id == todo_id) 
  await database.execute(query) 
  return {"message": "Todo ID: {} deleted successfully!".format(todo_id)} 