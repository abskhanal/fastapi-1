from fastapi import FastAPI
from fastapi import Body, Response, status, HTTPException, Depends

from typing import Optional

from pydantic import BaseModel

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

import pyodbc
import time

SERVER = 'BZCFR93LT'
DATABASE = 'BikeStores'

DRIVER = '{ODBC Driver 17 for SQL Server}'

connectionString = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

models.Base.metadata.create_all(bind=engine)







while True:
    try:
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        print("Connection Successful!")
        break
    except Exception as error:
        print(error)
        time.sleep(2)




app = FastAPI()

class Items(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str
    street: str
    city: str
    state: str
    zipcode: str


def get_dict(query):
    cursor = conn.cursor().execute(query)
    keys = [column[0] for column in cursor.description]
    values = cursor.fetchall()
    data = []
    for value in values:
        data_item = dict(zip(keys, value))
        data.append(data_item)
    return data

@app.get("/posts")
def read_root(db: Session = Depends(get_db)):
    query = """select * from sales.customers"""
    records = get_dict(query)
    return {"data":records}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/posts/{id}")
def get_posts(id: int):
    query = f"select * from sales.customers where customer_id = {id}"
    records = get_dict(query)     
    if records:
        return {"data":records}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} not found")


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Items):
    cursor = conn.cursor()
    cursor.execute(f"Insert into sales.customers (first_name, last_name, phone, email, street, city, state, zip_code) values (?,?,?,?,?,?,?,?)",post.firstname, post.lastname, post.phone, post.email, post.street, post.city, post.state, post.zipcode)
    #new_item = cursor.fetchone()
    conn.commit()
    return {"data":post}    

@app.put("/posts/{id}")
def update_post(id: int, post: Items):
    query1 = f"select * from sales.customers where customer_id = {id}"
    record = get_dict(query1)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} not found")
    
    cursor.execute(f" Update sales.customers set first_name = ?, last_name = ?, phone = ?, email=?, street=?, city=?, state=?, zip_code=? where customer_id = ?",post.firstname, post.lastname, post.phone, post.email, post.street, post.city, post.state, post.zipcode, id)  
    
    conn.commit()
    
    return {"data":f"{post} updated successfully"}  




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    query1 = f"select * from sales.customers where customer_id = {id}"
    record = get_dict(query1)
    
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} not found")
    
    query2 = f" Delete from sales.customers where customer_id = {id}" 
    cursor.execute(query2)
    conn.commit()
    return {"data":"Deleted successfully"}  
    
