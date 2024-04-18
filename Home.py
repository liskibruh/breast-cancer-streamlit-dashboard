## This script is not doing anything.
## The main scripts of the project is in the "pages" dir

import streamlit as st

st.set_page_config(page_title='Home')
st.title('This is the Home page')

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
