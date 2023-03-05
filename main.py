from fastapi import FastAPI
import connection
from bson import ObjectId
from pydantic import BaseModel
from typing import Union
# from schematics.models import Model
# from models import PyObjectId
import datetime

class Event(BaseModel):
    # event_id : ObjectId()
    event_name : str 
    event_location : str
    event_type : str
    event_date : datetime.date 
    event_description : Union[str, None] = None 
    event_capacity : Union[int, None] = None


# # An instance of class Event
# newevent = Event()

# # funtion to create and assign values to the instanse of class Event created
# def create_event(eventname):
#     # newevent.id = ObjectId()
#     newevent.name = eventname
#     return dict(newevent)


app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome To FastAPI World"}

@app.post("/event/{eventName}")
def addEvent(eventName: str):
    data = create_event(eventName)
    
    # Covert data to dict so it can be easily inserted to MongoDB
    dict(data)

    # # Checks if an email exists from the collection of users
    # if connection.db.users.find(
    #     {'email': data['email']}
    #     ).count() > 0:
    #     user_exists = True
    #     print("Customer Exists")
    #     return {"message":"Customer Exists"}
    # # If the email doesn't exist, create the user
    # elif user_exists == False:
    #     connection.db.users.insert_one(data)
    #     return {"message":"User Created","email": data['email'], "name": data['name']}

    # connection.db.events.insert_one(data)
    return {"message":"User Created","name": data['name']}

fake_items_db = [{"event_name": "Concerto Quim Barreiros", "event_location" : "Lisboa", "event_type" : "concert", "event_date" : "2023-05-17","event_description" : "Celebração dos 100 anos de carreira do icónico Quim Barreiros","event_capacity" : 10000 }, 
                 {"event_name": "Circo Cardinali", "event_location" : "Viseu", "event_type" : "entertainment","event_date" : "2023-11-17","event_description" : "Um espetáculo único com participação especial de Batatoon"}, 
                 {"event_name": "FC Porto - SL Benfica","event_location" : "Porto", "event_type" : "sport","event_date" : "2023-04-20", "event_description" : "Um clássico do futebol portugues a não perder", "event_capacity" : 55000}]

@app.get("/events/")
async def getEvents(skip: int = 0, limit: int = 10):
    print(fake_items_db[1]['event_name'])
    return fake_items_db[skip : skip + limit]


