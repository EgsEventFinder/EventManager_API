# from pydantic import BaseModel, Field as PydanticField
# from bson import ObjectId
import mongoengine
from mongoengine import DynamicDocument, Document, StringField, DateTimeField, IntField

class events(DynamicDocument):
    # id : ObjectId()
    event_id : StringField(required=True)
    name : StringField(max_length=100, required=True) 
    location : StringField(max_length=100) 
    type : StringField(max_length=100) 
    date : StringField(max_length=100) 
    description : StringField(max_length=100) = None
    capacity : IntField(max_length=100) = None

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")