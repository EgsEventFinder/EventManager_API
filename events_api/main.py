from fastapi import FastAPI, HTTPException, Query
# import connection
from bson import ObjectId
from pydantic import BaseModel
from typing import Union, Any, List, Optional
# from schematics.models import Model
# from models import PyObjectId
from models import events
from datetime import date, datetime, time
from mongoengine import connect
import json
# from bson.objectid import ObjectId
import os
from pymongo import MongoClient

app = FastAPI()

# MONGO_URI = os.getenv("MONGO_URI")

# client = MongoClient(MONGO_URI)
# db = client.mydatabase
con = connect(db='mydatabase', host='db', port=27017)


# client = MongoClient("mongodb://mongodb-container:27018/")
# db = client.mydatabase

# con = connect(db='Event_Manager', host='localhost', port=27017)
# collections=con['Event_Manager'].list_collection_names()

class EventCreate(BaseModel):
    name : str
    location : str
    type : str
    date : date 
    description : str
    capacity : int
    tickets : list

class EventUpdate(BaseModel):
    name: Optional[str] 
    location : Optional[str] 
    type : Optional[str] 
    date : Optional[date] 
    description : Optional[str] 
    capacity : Optional[int] 
    tickets : Optional[list]

@app.get("/")
def index():
    return {"message": "Welcome To Event_Manager_API my dear"}

fake_events_db = [{"id": "6404ed8b3f4e1034e1a0949e", "name": "Concerto Quim Barreiros", "location" : "Lisboa", "type" : "concert", "date" : "2023-05-17","description" : "Celebração dos 100 anos de carreira do icónico Quim Barreiros","capacity" : 10000, 
                "tickets": [
                {
                "type": "normal",
                "price": 10.00
                },
                {
                "type": "vip",
                "price": 30.00
                }
                ]}, 
                {"id": "6404ee613f4e1034e1a0949f", "name": "Circo Cardinali", "location" : "Viseu", "type" : "entertainment","date" : "2023-11-17","description" : "Um espetáculo único com participação especial de Batatoon", 
                "tickets": [
                {
                "type": "normal",
                "price": 20.00
                },
                {
                "type": "vip",
                "price": 50.00
                }
                ]}, 
                {"id": "6404eecb3f4e1034e1a094a0", "name": "FC Porto - SL Benfica","location" : "Porto", "type" : "sport","date" : "2023-04-20", "description" : "Um clássico do futebol portugues a não perder", "capacity" : 55000, 
                "tickets": [
                {
                "type": "normal",
                "price": 30.00
                },
                {
                "type": "vip",
                "price": 80.00
                }]}]

#, response_model=List[Event]
@app.get("/events")
async def getEvents(name: str = Query(None, alias="event_name"), 
                    type: str = Query(None, alias="event_type"),
                    skip: int = 0, 
                    limit: int = 10):
    
    ### Static version starts here 
    # print(fake_events_db[1]['name'])
    # return fake_events_db[skip : skip + limit]
    ### End of static version 
    
    query = {}
    if name:
        query['name__icontains'] = name
    if type:
        query['type__icontains'] = type

    # Query items with matching name and/or type
    if query:
        Events = events.objects(**query)
    else:
        Events = events.objects.skip(skip).limit(limit)
    
    return [e.to_dict() for e in Events]
    
    
@app.get("/events/{event_id}")
async def getEvent(event_id : str):
    ### Static version starts here 
    # for e in fake_events_db:
    #     if e['id'] == event_id:
    #         return e
        
    # raise HTTPException(status_code=404, detail="Event requested cannot be found in the system")
    ### End of static version 
    
    try:
        Events = events.objects.get(id = ObjectId(event_id))
        return Events.to_dict()
    except events.DoesNotExist:
        raise HTTPException(status_code=404, detail="Event requested cannot be found in the system")
        

@app.post("/events")
def addEvent(event : EventCreate):
    date_str = event.date.strftime("%Y-%m-%d")
    datetime_str = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=None)
    datetime_with_time = datetime.combine(datetime_str.date(), time.min)
    
    event = events.objects.create(id= str(ObjectId()), name=event.name, location=event.location, type=event.type, description=event.description, 
                                  date=datetime_with_time, capacity=event.capacity, tickets=event.tickets)

    return {"message":"Event Created", "Event": event.to_dict()}


@app.put("/events/{event_id}")
async def updateEvent(event_id: str, event_update: EventUpdate):
    try:
        event = events.objects.get(id=event_id)
        if event_update.name is not None:
            event.name = event_update.name
        if event_update.location is not None:
            event.location = event_update.location
        if event_update.type is not None:
            event.type = event_update.type
        if event_update.description is not None:
            event.description = event_update.description
        if event_update.date is not None:
            date_str = event_update.date.strftime("%Y-%m-%d")
            datetime_str = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=None)
            datetime_with_time = datetime.combine(datetime_str.date(), time.min)
            event.date = datetime_with_time
        if event_update.capacity is not None:
            event.capacity = event_update.capacity
        if event_update.tickets is not None:
            event.tickets = event_update.tickets    
        event.save()
        return {"message": f"Item with ID {event_id} updated successfully."}
    except events.DoesNotExist:
        return {"message": f"Item with ID {event_id} not found."}

@app.delete("/events/{event_id}")
async def deleteEvent(event_id: str):
    try:
        event = events.objects.get(id=event_id)
        event.delete()
        return {"message": f"Event with ID {event_id} deleted successfully."}
    except events.DoesNotExist:
        return {"message": f"Event with ID {event_id} not found."}


