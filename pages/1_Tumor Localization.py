import streamlit as st
import tensorflow as tf
import cv2
from PIL import Image
from numpy import asarray
import numpy as np


st.set_page_config(page_title='Tumor Localization')#, layout='wide')

#title
st.title('Breast Cancer Tumor Localization')

#load model function, set cache to prevent reloading
@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model('breast_tumor_segmentation_model.h5')
    return model

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

with st.spinner("Loading Model...."):
    model = load_model() #call load_model function to load the model

#image preprocessing function
def preprocess_image(img):
    size_x,size_y=128,128
    img = cv2.resize(img, (size_y, size_x))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = np.expand_dims(img, axis=0)
    return img

#ask user to upload image
file = st.file_uploader("Upload an ultrasound image ", type=['png','jpg','jpeg'])

if file is not None:
    image = Image.open(file) #open uploaded image
    image = asarray(image) #convert image to array

    prepd_img=preprocess_image(image) #preprocess image to meet the model's input requirements
    #original_img= prepd_img.reshape((128,128,3))
    #original_img= cv2.resize(original_img,(500,500))

    with st.spinner("Predicting..."):
        pred = model.predict(prepd_img) #pass the preprocessed image to the model to predict mask for it
        prediction_image = pred.reshape((128, 128, 1))
        prediction_image = cv2.resize(prediction_image,(500,500)) #resize the predicted mask image so it's displayed bigger on the web app page
    #display images
    col1, col2 = st.columns(2)
    col1.image(prepd_img)
    col2.image(prediction_image)