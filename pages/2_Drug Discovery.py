import streamlit as st
import json
from streamlit_lottie import st_lottie

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
