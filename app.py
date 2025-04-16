import streamlit as st
from PIL import Image
import os
from datetime import datetime
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "spartan-vine-456818-e9-ee2656c80875.json"
from bucket import upload_file
#from datastore import create_blood_cell_record
from google.cloud import pubsub_v1
from datastore import create_blood_cell_record
import re

os.makedirs("uploaded", exist_ok=True)

topic_path = 'projects/spartan-vine-456818-e9/topics/blood-cell-channel'
publisher = pubsub_v1.PublisherClient()

new_title = '<p style="font-family:sans-serif; color:Pink; font-size: 42px;">Blood Cell Detection </p>'
st.markdown(new_title, unsafe_allow_html=True)

st.image("1.png")
st.header("Detect Blood Cell")

email = st.text_input("Enter your email address")

def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

uploaded_file = st.file_uploader("Upload an image", type="jpg")

if st.button("Submit"):
    if not email or not is_valid_email(email):
        st.error("Please enter a valid email address.")
    elif not uploaded_file:
        st.error("Please upload an image file.")
    else:
        image = Image.open(uploaded_file)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"uploaded/image_{timestamp}.png"
        image.save(filename)

        upload_file(filename)
        record_id=create_blood_cell_record(email, filename)
        st.image(image, caption='Uploaded Image.', use_container_width=True)
        data = record_id.encode('utf-8')
        future = publisher.publish(topic_path, data)
        st.info("Hang tight! Your report is on the way and will arrive in your inbox shortly.")
