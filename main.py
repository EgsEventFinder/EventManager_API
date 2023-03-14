from fastapi import FastAPI, HTTPException, Query
import connection
from bson import ObjectId
from pydantic import BaseModel
from typing import Union, Any, List, Optional
# from schematics.models import Model
# from models import PyObjectId
from models import events
from datetime import date, datetime, time
from mongoengine import connect
import json
from bson.objectid import ObjectId


app = FastAPI()
con = connect(db='Event_Manager', host='localhost', port=27017)
collections=con['Event_Manager'].list_collection_names()

class EventCreate(BaseModel):
    name : str
    location : str
    type : str
    date : date 
    description : str
    capacity : int

class EventUpdate(BaseModel):
    name: Optional[str] 
    location : Optional[str] 
    type : Optional[str] 
    date : Optional[date] 
    description : Optional[str] 
    capacity : Optional[int] 

@app.get("/")
def index():
    return {"message": "Welcome To Event_Manager_API my dear"}

fake_items_db = [{"id": "6404ed8b3f4e1034e1a0949e", "name": "Concerto Quim Barreiros", "location" : "Lisboa", "type" : "concert", "date" : "2023-05-17","description" : "Celebração dos 100 anos de carreira do icónico Quim Barreiros","capacity" : 10000 }, 
                 {"id": "6404ee613f4e1034e1a0949f", "name": "Circo Cardinali", "location" : "Viseu", "type" : "entertainment","date" : "2023-11-17","description" : "Um espetáculo único com participação especial de Batatoon"}, 
                 {"id": "6404eecb3f4e1034e1a094a0", "name": "FC Porto - SL Benfica","location" : "Porto", "type" : "sport","date" : "2023-04-20", "description" : "Um clássico do futebol portugues a não perder", "capacity" : 55000}]

#, response_model=List[Event]
@app.get("/events")
async def getEvents(name: str = Query(None, alias="event_name"), 
                    type: str = Query(None, alias="event_type"),
                    skip: int = 0, 
                    limit: int = 10):
    # print(fake_items_db[1]['name'])
    # return fake_items_db[skip : skip + limit]
    
    
    # Events = json.loads(events.objects().to_json()) 
    # return {"events": Events}

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


    
@app.get("/event/{event_id}")
async def getEvent(event_id : str):
    try:
        Events = events.objects.get(id = ObjectId(event_id))
        return Events.to_dict()
    except events.DoesNotExist:
        raise HTTPException(status_code=404, detail="Event requested cannot be found in the system")
        
    # event_dict = {
    #     "event_id" : event.event_id,
    #     "name"  : event.name,
    #     "description" : event.description,
    #     "location"  : event.location,
    #     "type" : event.type,
    #     "date" : event.date,
    #     "capacity" : event.capacity
    # }

    # return event_dict



@app.post("/event")
def addEvent(event : EventCreate):
    date_str = event.date.strftime("%Y-%m-%d")
    datetime_str = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=None)
    datetime_with_time = datetime.combine(datetime_str.date(), time.min)
    
    event = events.objects.create(id= str(ObjectId()), name=event.name, location=event.location, type=event.type, description=event.description, 
                                  date=datetime_with_time, capacity=event.capacity)

    return {"message":"Event Created", "Event": event.to_dict()}


@app.put("/event/{event_id}")
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
        event.save()
        return {"message": f"Item with ID {event_id} updated successfully."}
    except events.DoesNotExist:
        return {"message": f"Item with ID {event_id} not found."}

@app.delete("/event/{event_id}")
async def deleteEvent(event_id: str):
    try:
        event = events.objects.get(id=event_id)
        event.delete()
        return {"message": f"Event with ID {event_id} deleted successfully."}
    except events.DoesNotExist:
        return {"message": f"Event with ID {event_id} not found."}



# TODO:
# event_id é o gerado pelo mongodb
# post events para adicionar um evento (alterar o atual)
# update endpoint (talvez com o endpoint events)
# events endpoint with query parameters event name and  event type
