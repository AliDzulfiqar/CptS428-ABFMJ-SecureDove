import uvicorn
import sys
import uuid
import psycopg2
import os


from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Union
from secrets import token_hex
from fastapi.middleware.cors import CORSMiddleware



# import sys to get more detailed Python exception info
import sys

# import the connect library for psycopg2
from psycopg2 import connect

# import the error handling libraries for psycopg2
from psycopg2 import OperationalError, errorcodes, errors




#First Instance of fastapi and the title for the docs page of FASTAPI
app = FastAPI(title="SecureDove Backend")




#Set up for connecting to the database
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

try:
        #Should really put line 50 into a secure file that doesn't go on github but until everyone can run this code i'll leave it in the file as is. Security wise this is bad procedure
        conn = psycopg2.connect('postgres://wjjloedt:JXFCuJI7Di3CtZ-enIemY9J_m8VxNXpZ@berry.db.elephantsql.com/wjjloedt')
        print('Connection Success!')
        connectionsucceeded = True
except:
    print("Unable to connect to the database")

# Open a cursor to execute SQL queries
cur = conn.cursor()




#default endpoint for the backend
@app.get("/")
def Default():
    return {"Default": "Test Data For SecureDove CptS 428"}


#This is a endpoint that allow you to query the database at a certain index that is passed in at the frontend by the user in messages.js
@app.get("/get_DB_info")
def get_DB_info(message_id: int):
    if message_id > 3:
         rows = [('We dont have messages at that index right now. Try 1-3',)]
         return {"data": rows}
    else:
        cur.execute(f"SELECT message_text FROM Messages WHERE message_id = {message_id};")
        rows = cur.fetchall()
        print(rows)
        return {"data": rows}

#Endpoint that adds a user to the Users table
@app.post("/registration")
async def registration(username: str, email: str, password: str):
    #Looping through Users until we find the lowest available user_id number
    cur.execute(f"SELECT * FROM Users")
    rows = cur.fetchall()
    i = 1
    for row in rows:
         if i == row[0]:
            i = i + 1
            continue
         else:
              break
    user_id = i
    print(user_id)
    #Inserting into the database
    cur.execute(f"INSERT INTO Users (user_id, username, email, password) VALUES ({user_id}, '{username}', '{email}', '{password}')")
    conn.commit()
    return {"success": True}

#Endpoint that deletes a user from the Users table
@app.delete("/delete_user")
def delete_user(username: str):
    cur.execute(f"SELECT username FROM Users")
    rows = cur.fetchall()
    if(username in rows):
        # Delete user based on username input
        cur.execute(f"DELETE FROM Users WHERE username = '{username}';")
        conn.commit()
        return {"accountDeletion":"Success"}
    return {"accountDeletion": "Failed"}


