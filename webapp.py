import streamlit as st 
import pandas as pd 
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
from PIL import Image

st.set_page_config(page_title='IT Dashboard', page_icon='ðŸ–¥',layout="wide")


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

hashed_pws = 'password'

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login","main")


if authentication_status:
    
    
        
    #Data source
    file = r'PATH_TO_FILE'

    df = pd.read_excel(file)
    
    df.rename(columns={'IP_Address_1':'IPv4'}, inplace=True)
    df.rename(columns={'Snapshot_Time':'Time'}, inplace=True)
    df.rename(columns={'Network_type1':'Network Type'}, inplace=True)
    df = df.sort_values(by=['User_Name'], inplace=False)
    columns = df.columns
    image = Image.open('logo.png')

    st.sidebar.image(image)
    
    st.title("IT Dashboard ")

    st.markdown('## User Logs')

    total_users, total_computers, empty3, empty4, empty5, empty6 = st.columns(6)
    with total_users:
        st.metric('Total Users', df['User_Name'].nunique())
    with total_computers:
        st.metric('Total Computers',  df['Host_Name'].nunique())



    group_by = st.sidebar.multiselect('Select Columns',columns,['Time', 'User_Name', 'Host_Name', 'IPv4','Network Type','Default_Gateway','System_Type','OS_Version','Free_Space','Boot_Time','Time_Stamp'])
    authenticator.logout('Logout', 'sidebar')
    # authenticator.logout('Logout','sidebar')

    df_grouped = df[group_by]

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
                
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    user_Name = st.multiselect(
        'Type the Domain_placeholder user name or PC/Host name below:',
        df_grouped['User_Name'].unique().tolist() + df_grouped['Host_Name'].unique().tolist())

    # host_Name = st.multiselect(
    #     'Type the PC name below:',
    #      df_grouped['Host_Name'].unique().tolist())

    df_selection = df_grouped.query("User_Name == @user_Name or Host_Name == @user_Name")

    if user_Name:
        st.dataframe(df_selection.reset_index(drop = True))
    else:
        st.dataframe(df_grouped.reset_index(drop = True), height=1500)
        
elif authentication_status == False:
    st.error('Username/password is incorrect')
    
elif authentication_status == None:
    st.warning('Please enter a valid username and password')
