# from pydantic import BaseModel, Field as PydanticField
# from bson import ObjectId
import mongoengine as db
from mongoengine import DynamicDocument, Document, StringField, DateField, IntField, ListField

class events(DynamicDocument):
    # id : ObjectId()
    id = db.ObjectIdField(required=True, primary_key=True)
    name : StringField(max_length=100, required=True) 
    location : StringField(max_length=100, required=False) 
    type : StringField(max_length=100, required=False) 
    date : DateField(required=False) 
    description : StringField(max_length=100, required=False) 
    capacity : IntField(required=False) 
    tickets : ListField(required=False)


    # def to_dict(self):
    #     """Converts the model instance to a dictionary."""
    #     result = {'id': str(self.id)}
    #     print(self._fields)
    #     for field_name in self._fields:
    #         result[field_name] = str(getattr(self, field_name))
    #     return result
    
    def to_dict(self):
        """Converts the model instance to a dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "location" : self.name,
            "type" : self.type,
            "date" : self.date,
            "description" : self.description,
            "capacity" : self.capacity,
            "tickets" : self.tickets
        }
    
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