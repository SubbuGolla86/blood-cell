import streamlit as st
from PIL import Image
import os
from datetime import datetime
from bucket import upload_file
from datastore import create_blood_cell_record

os.makedirs("uploaded", exist_ok=True)
os.makedirs("models", exist_ok=True)

new_title = '<p style="font-family:sans-serif; color:Pink; font-size: 42px;">Blood Cell Detection </p>'
st.markdown(new_title, unsafe_allow_html=True)

st.image("1.png")
st.header("Detect Blood Cell")

uploaded_file = st.file_uploader("Upload a image ", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"uploaded/image_{timestamp}.png"
    image.save(filename)
    upload_file(filename)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    record_id = create_blood_cell_record(user_name="John Doe",email="john@example.com",image_path=filename)
    data = st.info("Predicting Cancer......")
