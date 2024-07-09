import streamlit as st
import plotly.express as px 
import pandas as pd


st.set_page_config(
    page_title='Dashboard Page',
    page_icon='📈',
    layout='wide'
)
if st.session_state['authentication_status']:

    df = pd.read_csv('./Data/customer_churn_clean.csv')


    def eda_dashboard():
        st.markdown('#### Exploratory Data Analysis')

        col1, col2 = st.columns(2)

        with col1:
            # Group the data by 'Contact' and 'Churn' columns and count the occurrences of each category combination
            churn_by_contract = df.groupby(['Contract', 'Churn'])['Contract'].value_counts().reset_index(name='Count')
            # Create a grouped bar plot to visualize the count of churned and non-churned customers
            churn_by_contract = px.bar(churn_by_contract, x='Contract', y='Count', color='Churn', barmode='group', title='Customer Churn by Contract Terms')
            # Update layout
            churn_by_contract.update_layout(xaxis_title ='Contract', yaxis_title='Number of Customers')
            st.plotly_chart(churn_by_contract)

        with col2:
            tenure_churn = px.histogram(df, x='tenure', color='Churn', title='Relationship between Churn and Customer Tenure')
            tenure_churn.update_layout(yaxis_title='Count', xaxis_title='Tenure')
            st.plotly_chart(tenure_churn)

            
        col1, col2 = st.columns(2)
        with col1:
            # Create a box plot to visualize the distribution of Monthly Charges across churned and non-churned customers
            fig = px.box(df, x='Churn', y='MonthlyCharges', color='Churn', title='Distribution of Monthly Charges across Churn')

            # Set the y-axis label for better clarity
            fig.update_layout(yaxis_title='Monthly Charges')
            st.plotly_chart(fig)

        with col2:
            # Group the data by 'InternetService' and 'Churn' columns and calculate the sum of their monthly charges of each category combination
            mon_charge_by_internet_service = df.groupby(['InternetService', 'Churn'])['MonthlyCharges'].sum().reset_index(name='MonthlyCharge')

            # Create a grouped bar plot to visualize the monthly charge and count of churned and non-churned customers
            fig = px.bar(mon_charge_by_internet_service, x='InternetService', y='MonthlyCharge', color='Churn', barmode='group', title='Monthly Charges and Churn Rate by InternetService Type')

            # Update plot layout to set the x and y axes title
            fig.update_layout(xaxis_title='Internet Service Type', yaxis_title='Monthly Charge')
            st.plotly_chart(fig)    


    def kpi_dashboard():
        st.markdown('#### Key Performance Indicators')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div style="background-color: #CCE5FF; border-radius: 10px; width: 80%; margin-top: 20px;">
                    <h3 style="margin-left: 30px">Quick Stats About Dataset</h3>
                    <hr>
                    <h5 style="margin-left: 30px"> Churn Rate: {(df['Churn'].value_counts
                    (normalize=True).get("Yes", 0) * 100):.2f}%.</h5>
                    <hr>
                    <h5 style="margin-left: 30px">Average Monthly Charges: ${df['MonthlyCharges'].mean():.2f}</h5>
                    <hr>
                    <h5 style="margin-left: 30px">Total Revenue: ${df['TotalCharges'].sum():,.2f}</h5>
                    <hr>
                    <h5 style="margin-left: 30px"> Total Customers: {df['customerID'].nunique()}</h5>


                """,
                unsafe_allow_html=True,

            )
        with col2:
            pass




    if __name__ == '__main__':

        st.title("Dashboard")

        col1, col2 = st.columns(2)
        with col1:
            pass
        with col2:        
            st.selectbox('Select the type of Dashboard', options=['EDA', 'KPI'], 
            key='selected_dashboard_type')

        if st.session_state['selected_dashboard_type'] == 'EDA':
            eda_dashboard()
        else:
            kpi_dashboard()


elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app from the home page')
    




