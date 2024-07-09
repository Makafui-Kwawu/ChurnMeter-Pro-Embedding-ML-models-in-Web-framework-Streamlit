import streamlit as st 
import pyodbc
import pandas as pd
import time
from more_info import markdown_table


st.set_page_config(
    page_title='Data Page',
    page_icon='🛢️',
    layout='wide'
)

st.title('Customer Churn Database 🛢️')




# Create a connection database 
# query the database

@st.cache_resource(show_spinner='connecting to database...')
def init_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=" + st.secrets['SERVER'] + ";"
        "DATABASE=" + st.secrets['DATABASE'] + ";"
        "UID=" + st.secrets['USERNAME'] + ";"
        "PWD=" + st.secrets['PASSWORD'] + ";"
        "MARS_Connection=yes;"
        "MinProtocolVersion=TLSv1.2"
    )

connection = init_connection()


@st.cache_data(show_spinner='running_query...')
def running_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
    return df

def get_all_columns():
    sql_query = " SELECT * FROM LP2_Telco_churn_first_3000 "
    df = running_query(sql_query)

    return df

first_train = get_all_columns()

second_train = pd.read_csv("./Data/LP2_Telco-churn-second-2000.csv")

train_df = pd.concat([first_train,second_train])

# Define a dictionary for mapping boolean and None values to more meaningful categories
new_cat_values_mapping = {
    'multiple_lines': {True: 'Yes', False: 'No', None: 'No phone service'},
    'online_security': {True: 'Yes', False: 'No', None: 'No internet service'},
    'online_backup': {True: 'Yes', False: 'No', None: 'No internet service'},
    'device_protection': {True: 'Yes', False: 'No', None: 'No internet service'},
    'tech_support': {True: 'Yes', False: 'No', None: 'No internet service'},
    'streaming_tv': {True: 'Yes', False: 'No', None: 'No internet service'},
    'streaming_movies': {True: 'Yes', False: 'No', None: 'No internet service'},
    'churn': {True: 'Yes', False: 'No', None: 'No'},
    'partner': {True: 'Yes', False: 'No'},
    'dependents': {True: 'Yes', False: 'No'},
    'paperless_billing': {True: 'Yes', False: 'No'},
    'phone_service': {True: 'Yes', False: 'No'},
}

# Replace old categories with the new ones
train_df.replace(new_cat_values_mapping, inplace=True)


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













