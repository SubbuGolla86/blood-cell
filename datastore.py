from google.cloud import firestore
import uuid
from datetime import datetime

db = firestore.Client()

def create_blood_cell_record(user_name, email, image_path):
    record_id = str(uuid.uuid4())
    doc_ref = db.collection("Blood-cell-db").document(record_id)
    doc_ref.set({
        "id": record_id,
        "user_name": user_name,
        "email": email,
        "image_path": image_path,
        "timestamp": datetime.utcnow()
    })
    return record_id
