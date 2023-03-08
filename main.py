from fastapi import FastAPI, HTTPException
import connection
from bson import ObjectId
from pydantic import BaseModel
from typing import Union, Any, List
# from schematics.models import Model
# from models import PyObjectId
from models import events
import datetime
from mongoengine import connect
import json


app = FastAPI()
con = connect(db='Event_Manager', host='localhost', port=27017)
collections=con['Event_Manager'].list_collection_names()


@app.get("/")
def index():
    return {"message": "Welcome To Event_Manager_API my dear"}

fake_items_db = [{"event_id": "E100", "name": "Concerto Quim Barreiros", "location" : "Lisboa", "type" : "concert", "date" : "2023-05-17","description" : "Celebração dos 100 anos de carreira do icónico Quim Barreiros","capacity" : 10000 }, 
                 {"event_id": "E101", "name": "Circo Cardinali", "location" : "Viseu", "type" : "entertainment","date" : "2023-11-17","description" : "Um espetáculo único com participação especial de Batatoon"}, 
                 {"event_id": "E102", "name": "FC Porto - SL Benfica","location" : "Porto", "type" : "sport","date" : "2023-04-20", "description" : "Um clássico do futebol portugues a não perder", "capacity" : 55000}]

#, response_model=List[Event]
@app.get("/events")
async def getEvents(skip: int = 0, limit: int = 10):
    # print(fake_items_db[1]['name'])
    # return fake_items_db[skip : skip + limit]
    
    
    Events = json.loads(events.objects().to_json()) 
    return {"events": Events}

@app.get("/event/{event_id}")
async def getEvent(event_id : str):
    
    if(events.objects(event_id=event_id).first() is None):
        raise HTTPException(status_code=404, detail="Event requested cannot be found in the system")
    
    event = events.objects.get(event_id=event_id)

    event_dict = {
        "event_id" : event.event_id,
        "name"  : event.name,
        "description" : event.description,
        "location"  : event.location,
        "type" : event.type,
        "date" : event.date,
        "capacity" : event.capacity
    }

    return event_dict



@app.post("/event/{event_id}/{name}")
def addEvent(event_id : str, name: str):
    if(events.objects(event_id=event_id).first() is not None):
        # return {"message": "There's already an event with the given id!"} 
        raise HTTPException(status_code=401, detail="There's already an event in the system with the given id")
    
    event = events.objects.create(event_id=event_id, name=name)

    return {"message":"Event Created","event_id": event.event_id, "name" : event.name}

@app.delete("/event/{event_id}")
async def deleteEvent(event_id : str):
    
    if(events.objects(event_id=event_id).first() is None):
        raise HTTPException(status_code=404, detail="Event requested cannot be found in the system")
    
    events.objects(event_id=event_id).delete()

    return {"message":"Event deleted","event_id": event_id}
    






    # class Event(BaseModel):
#     # id : ObjectId()
#     name : str 
#     location : str
#     type : str
#     date : datetime.date 
#     description : Union[str, None] = None 
#     capacity : Union[int, None] = None


# # An instance of class Event
# newevent = Event()

# # funtion to create and assign values to the instanse of class Event created
# def create_event(eventname):
#     # newevent.id = ObjectId()
#     newevent.name = eventname
#     return dict(newevent)


    # for collection in collections:
    #     print (collection)

    # for e in events.objects():
    #     print (e.event_id, e.name, e.location, e.type, e.date, e.description, e.capacity)

    # data = create_event(eventName)
    
    # # Covert data to dict so it can be easily inserted to MongoDB
    # dict(data)

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
    # return {"message":"User Created","name": data['name']}



