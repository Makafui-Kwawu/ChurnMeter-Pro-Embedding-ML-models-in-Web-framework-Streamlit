#get libraries
import streamlit as st 
import requests
import json
from streamlit_lottie import st_lottie
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from Utils.info import column_1, column_2

st.set_page_config(
    page_title='Home Page',
    page_icon='🏠',
    layout='wide'
)


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)


name, authentication_status, username = authenticator.login(location='sidebar')


if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')
    st.title('ChurnMeter-Pro!')

    col1, col2 = st.columns(2)
    with col1:
        column_1
    with col2:
        column_2

        #define function to get animation
    def lottie_url(url:str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    lottie_img = lottie_url("https://lottie.host/80d6a368-c787-4f59-8eca-9b649cf41b1b/VdfzfJeXsp.json")


    
    with st.container():
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            st.header("About us")
            st.write("##")
            st.write("""
                    Our group of experts in the team operate with the following objectives:

                    - Explore our clients data thoroughly and decide on the most efficient classification models.
                    - Find the lifetime value of each customer and know what factors affect the rate at which customers stop using their network.
                    - Predict if a customer will churn or not.""")
        with col2:
            st_lottie(
        lottie_img,
        speed=1,
        reverse= False,
        loop=True,
        quality="high",
        key="coding",
        height=500,
        width=600

    )

    with st.container():
            st.write("---")
            st.header("Explore")
            st.write("##")
            st.write("With our powerful machine learning algorithms, you could also try to predict whether a customer will churn or not with your own dataset!")
            st.write("##")
            uploaded_file = st.file_uploader("Upload your file here")


    # Initialize authentication status
    if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None        


elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app')
    st.code("""
        Test Account
        Username: makafui-kwawu
        Password: 123456
        """)




