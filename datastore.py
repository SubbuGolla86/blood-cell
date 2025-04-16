from google.cloud import datastore
import uuid
from datetime import datetime

datastore_client = datastore.Client()
kind_name = "blood-cell-db"

def create_blood_cell_record( email, image_path):
     record_id = str(uuid.uuid4())
     key = datastore_client.key(kind_name, record_id)
     entity = datastore.Entity(key=key)
     entity.update({
         "id": record_id,
         "email": email,
         "image_path": image_path,
         "status" : "processing",
         "result" : "",
         "timestamp": datetime.utcnow()
     })
     datastore_client.put(entity)
     return record_id
