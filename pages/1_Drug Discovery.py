import streamlit as st
import json
from streamlit_lottie import st_lottie
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import shlex
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
st.title('Drug Discovery (Aromatase Inhibitors)')

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

################################## functions ######################################
# Molecular descriptor calculator
def desc_calc():
    # Performs the descriptor calculation
    #bashCommand = "java.exe -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"

    bashCommand = "java.exe -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
    #subprocess_cmd = shlex.split(bashCommand)
    #subprocess.call(subprocess_cmd)
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
    load_model = pickle.load(open('DrugDiscovery_Aromatase_52 (1).pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    ####molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.DataFrame(prediction_output)
    ####df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

######################################## col 1 ########################################################
col1, col2 = st.columns(2)
with col1:
    st.subheader('Upload a file that contains the SMILES notation')
    uploaded_file = st.file_uploader('Upload .txt file', type = ['txt'], label_visibility='collapsed')
    # load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    # st.write(load_data)
    st.markdown("""
    [Download this example file as .txt](https://raw.githubusercontent.com/liskibruh/breast-cancer-streamlit-dashboard/main/example_smiles.txt)
    """)
    
    if st.button('Predict'):
        load_data = pd.read_table(uploaded_file, sep=' ', header=None)
        load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)

        st.header('**Original input data**')
        st.write(load_data)

        with st.spinner("Calculating descriptors..."):
            desc_calc()
        # Read in calculated descriptors and display the dataframe
        st.header('**Calculated molecular descriptors**')
        desc = pd.read_csv('descriptors_output.csv')
        st.write(desc)
        st.write(desc.shape)

        # Read descriptor list used in previously built model
        st.header('**Descriptors after dimensionality reduction**')
        Xlist = list(pd.read_csv('descriptor_list.csv').columns)
        desc_subset = desc[Xlist]
        st.write(desc_subset)
        st.write(desc_subset.shape)

        # Apply trained model to make prediction on query compounds
        build_model(desc_subset)
    else:
        st.info('Upload data to start!')

########################################## col2 ########################################################

with col2:
    a=None
    st.subheader('OR write the SMILES notation in the text box below')
    smiles_text = st.text_input(
            'Enter SMILE',
            max_chars=100,
        )
    no_of_chars=len(smiles_text)
    st.write('Example SMILE: CC12CCC(O)CC1=CCC1C2CCC2(C)C(CC3CN3)CCC12')

    if st.button('Predict',key=2):
        st.write('SMILE:', smiles_text)
        st.write('Number of characters: ', no_of_chars)
        # Create a DataFrame with the string
        load_data = pd.DataFrame({'SMILES': [smiles_text]})

        # Export the DataFrame to a CSV file
        load_data.to_csv('molecule.smi',header = False, index = False)

        st.header('**Original input data**')
        st.write(load_data)
        
        with st.spinner("Calculating descriptors..."):
            desc_calc()
        # Read in calculated descriptors and display the dataframe
        st.header('**Calculated molecular descriptors**')
        desc = pd.read_csv('descriptors_output.csv')
        st.write(desc)
        st.write(desc.shape)

        # Read descriptor list used in previously built model
        st.header('**Descriptors after dimensionality reduction**')
        Xlist = list(pd.read_csv('descriptor_list.csv').columns)
        desc_subset = desc[Xlist]
        st.write(desc_subset)
        st.write(desc_subset.shape)

        # Apply trained model to make prediction on query compounds
        build_model(desc_subset)

    else:
        st.info('Input data to start!')