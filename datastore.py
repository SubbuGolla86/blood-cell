from google.cloud import datastore
import uuid
from datetime import datetime
import pandas as pd

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


def fetch_records_by_email(email):
    query = datastore_client.query(kind=kind_name)
    query.add_filter("email", "=", email)
    results = list(query.fetch())

    if results:
        data = []
        for entity in results:
            data.append({
                "id": entity["id"],
                "email": entity["email"],
                "image_path": entity["image_path"],
                "status": entity["status"],
                "result": entity["result"],
                "timestamp": entity["timestamp"]
            })

        df = pd.DataFrame(data)
        return df
    else:
        return pd.DataFrame(columns=["id", "email", "image_path", "status", "result", "timestamp"])
