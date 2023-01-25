import streamlit as st
from streamlit_lottie import st_lottie
import json

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

st.title('This is the Cancer Classification page')

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)