import streamlit as st
import json
from streamlit_lottie import st_lottie
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle

st.set_page_config(page_title='Drug Discovery', layout='wide')

#add lottie animation
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

lottie_file = load_lottiefile('18944-discovery.json')
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

#title
st.title('This is the Drug Discovery page')

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

################################## functions ######################################
# Molecular descriptor calculator
def desc_calc():
    # Performs the descriptor calculation
    bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove('molecule.smi')

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Model building
def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

######################################################################################
col1, col2 = st.columns(2)
with col1:
    st.subheader('Upload a file that contains the SMILES notation')
    uploaded_file = st.file_uploader('Upload .txt file', type = ['txt'], label_visibility='collapsed')
    
    if st.button('Predict'):
        pass

with col2:
    st.subheader('OR write the SMILES notation in the text box below')
    smiles_text = st.text_input(
            'Enter SMILES',
            max_chars=50,
        )

    if st.button('Predict',key=2):
        pass

