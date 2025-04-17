import streamlit as st
from PIL import Image
import os
from datetime import datetime
import re
from google.cloud import pubsub_v1
from bucket import upload_file
from datastore import create_blood_cell_record,fetch_records_by_email

os.makedirs("uploaded", exist_ok=True)

topic_path = 'projects/spartan-vine-456818-e9/topics/blood-cell-channel'
publisher = pubsub_v1.PublisherClient()

# Helper function to validate email
def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)


def home_page():
    new_title = '<p style="font-family:sans-serif; color:Pink; font-size: 42px;">Blood Cell Detection </p>'
    st.markdown(new_title, unsafe_allow_html=True)
    
    st.image("1.png")
    st.header("Welcome to the Blood Cell Detection Platform")
    st.write("""
    This platform allows you to upload images of blood cells for automated detection and reporting.
    The system will analyze your uploaded image, detect blood cells, and provide you with a report shortly.
    Please enter your email and upload a clear image for analysis.
    """)

def predict_page():
    st.header("Detect Blood Cell")
    email = st.text_input("Enter your email address")
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
             st.info("Hang tight! Your report is on the way. Please check the history.")

def history_page():
    email = st.text_input("Enter your email address")
    if st.button("Submit"):
        if not email or not is_valid_email(email):
            st.error("Please enter a valid email address.")
        else:    
            df = fetch_records_by_email(email)
            st.write("Your history:")
            st.dataframe(df)



page = st.sidebar.radio("Select a page", ["Home", "Predict Blood Cells", "History"])

if page == "Home":
    home_page()
elif page == "Predict Blood Cells":
    predict_page()
elif page == "History":
    history_page()
