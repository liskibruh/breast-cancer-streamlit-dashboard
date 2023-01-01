import streamlit as st

st.set_page_config(page_title='Cancer Detection')

st.title('This is the Cancer Detection page')

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)