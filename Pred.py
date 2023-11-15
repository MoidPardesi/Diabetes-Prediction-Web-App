import numpy as np
import pickle
import pandas as pd
import streamlit as st
from joblib import load

# loading the saved model
loaded_model = load('GradientBoostingClassifier.joblib')


# creating a function for Prediction

def diabetes_prediction(input_data):
    # Create a DataFrame from the input data
    new_data = pd.DataFrame([input_data], columns=['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 
                                                   'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 
                                                   'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth',
                                                    'MentHlth', 'PhysHlth','DiffWalk', 
                                                   'Sex', 'Age', 'Education','Income'])

    # Make a prediction
    prediction = loaded_model.predict(new_data)

    if prediction[0] == 0:
        return 'The person is not diabetic'
    elif prediction[0] == 1:
        return 'The person is prediabetic'
    else:
        return 'The person is diabetic'
    
  
def main():
   st.title('Diabetes Prediction Web App')
   st.markdown("Welcome to the Diabetes Prediction Web App. Please enter the information below to assess your diabetes risk:")
   with st.form("prediction_form"):
    st.subheader('Health Information')

    
    col1, col2 = st.columns(2)

    with col1:
        HighBP = st.radio('High Blood Pressure', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        HighChol = st.radio('High Cholesterol', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        CholCheck = st.radio('Cholesterol Check in Last 5 Years', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        BMI = st.number_input('Body Mass Index (BMI)', min_value=0.0, max_value=100.0, value=25.0, step=0.1)
        Smoker = st.radio('Smoker (100 cigarettes in lifetime)', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        Stroke = st.radio('History of Stroke', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        HeartDiseaseorAttack = st.radio('Heart Disease or Attack', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        PhysActivity = st.radio('Physical Activity in Last 30 Days', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        DiffWalk = st.radio('Difficulty Walking', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        age_groups = {'18-24':1, '25-29':2, '30-34':3, '35-39':4, '40-44':5, '45-49':6,
                       '50-54':7, '55-59':8, '60-64':9, '65-69':10, '70-74':11, '75-79':12, '>80':13}
        Age = st.selectbox('Age Group', list(age_groups.keys()))
        education_levels = {
            'Never attended school or only kindergarten':1,
            'Grades 1 through 8 (Elementary)':2,
            'Grades 9 through 11 (Some high school)':3,
            'Grade 12 or GED (High school graduate)':4,
            'College 1 year to 3 years (Some college or technical school)':5,
            'College 4 years or more (College graduate)':6}
        Education = st.selectbox('Education Level',list(education_levels.keys()))
            
    with col2:
        Fruits = st.radio('Daily Fruits Consumption', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        Veggies = st.radio('Daily Vegetables Consumption', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        HvyAlcoholConsump = st.radio('Heavy Alcohol Consumption (Men >14 drinks/week, Women >7 drinks/week)', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        AnyHealthcare = st.radio('Access to Healthcare', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        NoDocbcCost = st.radio('Could not see Doctor due to Cost', [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            
        GenHlth = st.select_slider('General Health', options=[1, 2, 3, 4, 5], format_func=lambda x: {1: 'Excellent', 2: 'Very Good', 3: 'Good', 4: 'Fair', 5: 'Poor'}[x])
        MentHlth = st.number_input('Mental Health (Days not good in last 30 days)', min_value=0, max_value=30, value=0, step=1)
        PhysHlth = st.number_input('Physical Health (Days not good in last 30 days)', min_value=0, max_value=30, value=0, step=1)
        Sex = st.radio('Gender', [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
        income_scale = {
            'Less than $10,000':1,
            '$10,000 to $14,999':2,
            '$15,000 to $19,999':3,
            '$20,000 to $24,999':4,
            '$25,000 to $34,999':5,
            '$35,000 to $49,999':6,
            '$50,000 to $74,999':7,
            '$75,000 or more':8}
        Income = st.selectbox('Income Scale',list(income_scale.keys()))

        
        # Submit button for the form
        submitted = st.form_submit_button("Diabetes Test Result")
        if submitted:
            Age_numeric = age_groups[Age]
            Education_numeric = education_levels[Education]
            Income_numeric = income_scale[Income]
            diagnosis = diabetes_prediction([
                HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity,
                Fruits, Veggies, HvyAlcoholConsump, AnyHealthcare, NoDocbcCost, GenHlth, MentHlth, PhysHlth,
                DiffWalk, Sex, Age_numeric, Education_numeric, Income_numeric
            ])
            
            # Display result with conditional formatting
            if diagnosis == 'The person is diabetic':
                st.error(diagnosis)     
            elif diagnosis == 'The person is prediabetic':
                st.warning(diagnosis)
            else:
                st.success(diagnosis)

if __name__ == '__main__':
    main()
