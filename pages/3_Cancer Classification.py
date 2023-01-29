import streamlit as st
import tensorflow as tf
import cv2
from PIL import Image
from numpy import asarray
import numpy as np
import json
from streamlit_lottie import st_lottie

#title
st.set_page_config(page_title='Cancer Classification', layout='wide')

#add lottie animation
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

lottie_file = load_lottiefile('33758-dashboard.json')
col1, col2, col3= st.columns(3)
with col1:
    st_lottie(
    lottie_file,
    reverse=False,
    loop=True,
    quality='low',
    height=100,
    width=200
)

st.title('Cancer Classification (Images)')

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#####################################################################################################################
#load model function, set cache to prevent reloading
@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model('CancerClassification.h5')
    return model

with st.spinner("Loading Model...."):
    model = load_model() #call load_model function to load the model

#image preprocessing function
def preprocess_image(img):
    size_x,size_y=227,227
    img = asarray(img) #convert image to array
    img = cv2.resize(img, (size_y, size_x))
    img = np.expand_dims(img, axis=-1)
    img = np.dstack([img, img, img])
    img = np.expand_dims(img, axis=0)
    
    return img

#ask user to upload image
file = st.file_uploader("Upload an MRI image ", type=['png','jpg','jpeg'])    
st.markdown("""
[Download Example Image](https://github.com/liskibruh/breast-cancer-streamlit-dashboard/blob/main/malignant_example.png)
""")


if file is not None:
    image = Image.open(file) #open uploaded image
    image_temp = asarray(image)
    #st.write(image_temp.shape)

    prepd_img=preprocess_image(image) #preprocess image to meet the model's input requirements
    
    # #display images
    col1, col2 = st.columns(2)
    with col1:
        st.image(prepd_img)

    with col2:
        with st.spinner("Predicting..."):
            pred = model.predict(prepd_img) #pass the preprocessed image to the model to predict mask for it
            pred=int(np.argmax(pred,axis=1))
            #st.subheader(pred)
            if(pred==0 or pred==2 or pred==4 or pred==6):
                st.metric(label = 'Breast Cancer Type',value = 'Benign')
            elif(pred==1 or pred==3 or pred==5 or pred==7):
                st.metric(label = 'Breast Cancer Type', value = 'Malignant')