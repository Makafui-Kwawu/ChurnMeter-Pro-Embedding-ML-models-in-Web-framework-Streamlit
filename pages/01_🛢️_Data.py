import streamlit as st 
import pyodbc
import pandas as pd
import time
from Utils.more_info import markdown_table


st.set_page_config(
    page_title='Data Page',
    page_icon='🛢️',
    layout='wide'
)

if st.session_state['authentication_status']:
    

    st.title('Customer Churn Database 🛢️')

    # Load dataset
    train_df = pd.read_csv("./Data/customer_churn_clean.csv")


    #create a progress bar to let user know data is loading
    progress_bar = st.progress(0)
    for perc_completed in range(100):
        time.sleep(0.05)
        progress_bar.progress(perc_completed+1)

    st.success("Data loaded successfully!")



    #grouping all numeric columns
    numerics = train_df.select_dtypes("number").columns
    #grouping all categorical columns
    categoricals = train_df.select_dtypes("object").columns


    option = st.selectbox(
        "How would you like to view data?",
        ("All data", "Numerical columns", "Categorical columns"),
        index=None,
        placeholder="Select contact method...",)
    # Conditionally display data based on the selected option
    if option == "All data":
        st.write("### All Data")
        st.dataframe(train_df)
        if st.button("Click here to get more information about data dictionary"):
            # Display the markdown table inside the expander
            st.markdown(markdown_table)
    elif option == "Numerical columns":
        st.write("### Numerical Columns")
        st.dataframe(train_df[numerics])
        if st.button("Click here to get more information about data dictionary"):
            # Display the markdown table inside the expander
            st.markdown(markdown_table)
    elif option == "Categorical columns":
        st.write("### Categorical Columns")
        st.dataframe(train_df[categoricals])
        if st.button("Click here to get more information about data dictionary"):
            # Display the markdown table inside the expander
            st.markdown(markdown_table)


elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app from the home page')
    












