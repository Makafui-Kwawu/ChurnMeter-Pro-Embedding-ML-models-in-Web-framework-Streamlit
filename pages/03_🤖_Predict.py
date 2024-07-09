import streamlit as st
import pandas as pd
import joblib
import os
import datetime


st.set_page_config(
    page_title='Predict Page',
    page_icon='🤖',
    layout='wide'
)


if st.session_state['authentication_status']:
    st.title("Predict Customer Churn")

    @st.cache_resource()
    def load_logistic_pipeline():
        return joblib.load('models/logistic_pipeline.joblib')

    @st.cache_resource()
    def load_gradient_pipeline():
        return joblib.load('models/gradient_pipeline.joblib')

    @st.cache_resource(show_spinner='Models Loading....')
    def load_encoder():
        return joblib.load('models/encoder.joblib')

    def select_model():
        col1, col2 = st.columns(2)

        with col1:
            st.selectbox('Select a model', options=['Logistic Regression', 'Gradient Boosting Classifier'], key='selected_model')
        with col2:
            pass

        if st.session_state['selected_model'] == 'Logistic Regression':
            pipeline = load_logistic_pipeline()
        else:
            pipeline = load_gradient_pipeline()

        encoder = load_encoder()
        
        return pipeline, encoder

    def make_prediction(pipeline, encoder):
        # Collect input data from session state
        gender = st.session_state['gender']
        SeniorCitizen = 1 if st.session_state['SeniorCitizen'] == 'Yes' else 0
        Partner = st.session_state['Partner']
        Dependents = st.session_state['Dependents']
        Contract = st.session_state['Contract']
        tenure = st.session_state['tenure']
        PhoneService = st.session_state['PhoneService']
        MultipleLines = st.session_state['MultipleLines']
        InternetService = st.session_state['InternetService']
        OnlineSecurity = st.session_state['OnlineSecurity']
        OnlineBackup = st.session_state['OnlineBackup']
        DeviceProtection = st.session_state['DeviceProtection']
        TechSupport = st.session_state['TechSupport']
        StreamingTV = st.session_state['StreamingTV']
        StreamingMovies = st.session_state['StreamingMovies']
        MonthlyCharges = st.session_state['MonthlyCharges']
        TotalCharges = st.session_state['TotalCharges']
        PaperlessBilling = st.session_state['PaperlessBilling']
        PaymentMethod = st.session_state['PaymentMethod']

        # Create the data and DataFrame
        data = [[gender, SeniorCitizen, Partner, Dependents, Contract, tenure, PhoneService,
                MultipleLines, InternetService, OnlineSecurity, OnlineBackup,
                DeviceProtection, TechSupport, StreamingTV, StreamingMovies, MonthlyCharges, TotalCharges, PaperlessBilling, PaymentMethod]]

        columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Contract', 'tenure',
                'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'MonthlyCharges',
                'TotalCharges', 'PaperlessBilling', 'PaymentMethod']

        df = pd.DataFrame(data, columns=columns)

        # Make predictions and get probabilities
        pred = pipeline.predict(df)
        pred_int = int(pred[0])

        prediction = encoder.inverse_transform([pred_int])
        probability = pipeline.predict_proba(df)

        # Update session state with prediction and probability
        st.session_state['prediction'] = prediction[0]
        st.session_state['probability'] = probability[0]

        # Prepare DataFrame for logging
        df['prediction'] = prediction[0]
        df['probability_yes'] = probability[0][1]  # Probability of positive class
        df['probability_no'] = probability[0][0]   # Probability of negative class
        df['time_of_prediction'] = datetime.date.today()
        df['model_used'] = st.session_state['selected_model']

        # Save DataFrame to CSV
        df.to_csv('./Data/history.csv', mode='a', header=not os.path.exists('./Data/history.csv'), index=False)

        return prediction[0], probability[0]

    # Display form and handle inputs
    def display_form():
        pipeline, encoder = select_model()

        with st.form('input_features'):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.write("**DEMOGRAPHIC INFO**")
                st.selectbox('Gender', options=['Male', 'Female'], key='gender')
                st.selectbox('Senior Citizen', options=['Yes', 'No'], key='SeniorCitizen')
                st.selectbox('Partner', options=['Yes', 'No'], key='Partner')
                st.selectbox('Dependents', options=['Yes', 'No'], key='Dependents')

            with col2:
                st.write("**CONTRACT & PHONE SERVICES**")
                st.selectbox('Contract', options=["Month-to-month", "One year", "Two year"], key='Contract')
                st.number_input('Tenure', key='tenure', min_value=1, max_value=72, step=1)
                st.selectbox('Phone Service', options=["Yes", "No"], key='PhoneService')
                st.selectbox('Multiple Lines', options=["Yes", "No"], key='MultipleLines')

            with col3:
                st.write("**INTERNET SERVICES**")
                st.selectbox('Internet Service', options=["DSL", "Fiber optic", "No"], key='InternetService')
                st.selectbox('Online Security', options=["Yes", "No"], key='OnlineSecurity')
                st.selectbox('Online Backup', options=["Yes", "No"], key='OnlineBackup')
                st.selectbox('Device Protection', options=["Yes", "No"], key='DeviceProtection')
                st.selectbox('Tech Support', options=["Yes", "No"], key='TechSupport')
                st.selectbox('Streaming TV', options=["Yes", "No"], key='StreamingTV')
                st.selectbox('Streaming Movies', options=["Yes", "No"], key='StreamingMovies')

            with col4:
                st.write("**BILLING AND PAYMENT INFO**")
                st.number_input('Monthly Charges', key='MonthlyCharges', step=0.05)
                st.number_input('TotalCharges', key='TotalCharges', step=0.05)
                st.selectbox('Paperless Billing', options=["Yes", "No"], key='PaperlessBilling')
                st.selectbox('Payment Method', options=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], key='PaymentMethod')

            st.form_submit_button('Submit', on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))

    if __name__ == '__main__':
        # Ensure 'prediction' and 'probability' keys exist in session_state
        if 'prediction' not in st.session_state:
            st.session_state['prediction'] = None
        if 'probability' not in st.session_state:
            st.session_state['probability'] = None

        display_form()

        final_prediction = st.session_state['prediction']
        probability = st.session_state['probability']

        if final_prediction is None:
            st.write('### Predictions show here!')
            st.divider()
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f'### Prediction: {final_prediction}')
            with col2:
                st.write(f'### Probability: {round(probability[1], 2) if final_prediction == "Yes" else round(probability[0], 2)}')

        st.divider()

        st.write(st.session_state)

elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app from the home page')
      
