import streamlit as st

st.set_page_config(page_title='Home')
st.title('This is the The Team page')

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)