import streamlit as st
import pickle

st.set_page_config(page_title='About', layout='wide')
st.title('Cancer Classification (Tabular)')

#apply css from style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def build_model(input_data):
    # Reads in saved model
    load_model = pickle.load(open('breast_cancer_classificationRForst99.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    return prediction

########################################################################################
"""             'radius_mean', 'texture_mean', 'perimeter_mean',
                'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean',
                'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
                'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
                'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
                'fractal_dimension_se', 'radius_worst', 'texture_worst',
                'perimeter_worst', 'area_worst', 'smoothness_worst',
                'compactness_worst', 'concavity_worst', 'concave points_worst'
"""

values = st.text_input(
    'Enter Values',
    max_chars=1000
) 
st.write('Example Input: 1.340e+01,2.052e+01,8.864e+01,5.567e+02,1.106e-01,1.469e-01,1.445e-01,8.172e-02,2.116e-01,7.325e-02,3.906e-01,9.306e-01,3.093e+00,3.367e+01,5.414e-03,2.265e-02,3.452e-02,1.334e-02,1.705e-02,4.005e-03,1.641e+01, 2.966e+01,1.133e+02,8.444e+02,1.574e-01,3.856e-01,5.106e-01,2.051e-01,3.585e-01,1.109e-01') 
if st.button('Predict'):
    if len(values) > 100:
        values_list = values.split(',')
        values_list = [float(x) for x in values_list]
        values_list = [values_list]
        prediction=build_model(values_list)
        if prediction==0:
            st.metric('Cancer Type', 'Benign')
        elif prediction==1:
            st.metric('Cancer Type', 'Malignant')

    else:
        st.info('Check your input values')