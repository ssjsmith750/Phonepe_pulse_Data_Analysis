import pandas as pd 
import plotly.express as px
import streamlit as st 
import mysql.connector
import plotly.graph_objects as go

PhonePe=mysql.connector.connect(host='localhost',
                        database='phonepe',
                        user='root',
                        password='****')
mycursor = PhonePe.cursor()
st.title('PhonePe Pulse  and User Transaction Data Analysis(2018-2022):signal_strength:')
st.write("### :blue[PHONEPE TASK]")
# Retrieve Data From Database
query = 'select * from Map_Transaction_Table'
Map_Transaction_Table_df = pd.read_sql(query, con = PhonePe)
query = 'select * from Map_Districts_GeoLocation'
Districts_GeoLocation = pd.read_sql(query, con = PhonePe)
query = 'select * from Map_IndianStatesTotal_Users'
Map_IndianStatesTotal_Users_df = pd.read_sql(query, con = PhonePe)
query = 'select * from Aggregated_Transaction'
Aggregated_Transaction_df=pd.read_sql(query, con = PhonePe)
query = 'select * from Aggregated_User_Table'
Aggregated_User_df=pd.read_sql(query, con = PhonePe)
query = 'select * from Aggregated_User_Summary'
Aggregated_User_Summary_df=pd.read_sql(query, con = PhonePe)
query = 'select * from State_Geo_Location_Data'
State_Geo_Location_Data_df=pd.read_sql(query, con = PhonePe)

st.title(':blue[PhonePe Pulse Data Analysis(2018-2022):signal_strength:]')
st.write("### **:blue[PhonePe India]**")
Year = st.selectbox(
    'Please select the Year',
    ('2018', '2019', '2020','2021','2022'))
Quarter = st.selectbox(
    'Please select the Quarter',
    ('1', '2', '3','4'))
year=int(Year)
quarter=int(Quarter)
Districtwise_MapTransaction=Map_Transaction_Table_df.loc[(Map_Transaction_Table_df['Year'] == year ) & (Map_Transaction_Table_df['Quarter']==quarter) ].copy()
Statewise_Transaction=Districtwise_MapTransaction[Districtwise_MapTransaction["State"] == "india"]
Districtwise_MapTransaction.drop(Districtwise_MapTransaction.index[(Districtwise_MapTransaction["State"] == "india")],axis=0,inplace=True)

# Districtwise_MapTransaction
Districtwise_MapTransaction = Districtwise_MapTransaction.sort_values(by=['Place_Name'], ascending=False)
Districts_GeoLocation = Districts_GeoLocation.sort_values(by=['District'], ascending=False) 
Total_Amount=[]
for i in Districtwise_MapTransaction['Total_Amount']:
    Total_Amount.append(i)
Districts_GeoLocation['Total_Amount']=Total_Amount
Total_Transaction=[]
for i in Districtwise_MapTransaction ['Total_Transactions_count']:
    Total_Transaction.append(i)
Districts_GeoLocation['Total_Transactions']=Total_Transaction
Districts_GeoLocation['Year_Quarter']=str(year)+'-Q'+str(quarter)

# Map_IndianStatesTotal_Users_df
Map_IndianStatesTotal_Users_df = Map_IndianStatesTotal_Users_df.sort_values(by=['state'], ascending=False)
Statewise_Transaction = Statewise_Transaction.sort_values(by=['Place_Name'], ascending=False)
Total_Amount=[]
for i in Statewise_Transaction['Total_Amount']:
    Total_Amount.append(i)
Map_IndianStatesTotal_Users_df['Total_Amount']=Total_Amount
Total_Transaction=[]
for i in Statewise_Transaction['Total_Transactions_count']:
    Total_Transaction.append(i)
Map_IndianStatesTotal_Users_df['Total_Transactions']=Total_Transaction
"*****************************************MAP********************************************"
#scatter plotting the states codes 
State_Geo_Location_Data_df = State_Geo_Location_Data_df.sort_values(by=['state'], ascending=False)
State_Geo_Location_Data_df['Registered_Users']=Map_IndianStatesTotal_Users_df['Registered_Users']
State_Geo_Location_Data_df['Total_Amount']=Map_IndianStatesTotal_Users_df['Total_Amount']
State_Geo_Location_Data_df['Total_Transactions']=Map_IndianStatesTotal_Users_df['Total_Transactions']
State_Geo_Location_Data_df['Year_Quarter']=str(year)+'-Q'+str(quarter)
fig=px.scatter_geo(State_Geo_Location_Data_df,
                   lon=State_Geo_Location_Data_df['Longitude'],
                   lat=State_Geo_Location_Data_df['Latitude'],                                
                   text = State_Geo_Location_Data_df['code'], #It will display district names on map
                   hover_name="state", 
                   hover_data=["Registered_Users",'Total_Amount',"Total_Transactions","Year_Quarter"],
                   )
fig.update_traces(marker=dict(color="white" ,size=0.3))
fig.update_geos(fitbounds="locations", visible=False,)
# scatter plotting districts
Districts_GeoLocation['col']=Districts_GeoLocation['Total_Transactions']
fig1=px.scatter_geo(Districts_GeoLocation,
                   lon=Districts_GeoLocation['Longitude'],
                   lat=Districts_GeoLocation['Latitude'],
                   color=Districts_GeoLocation['col'],
                   size=Districts_GeoLocation['Total_Transactions'],     
                   #text = Districts_GeoLocation['District'], #It will display district names on map
                   hover_name="District", 
                   hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                   title='District',
                   size_max=22,)
fig1.update_traces(marker=dict(color="rebeccapurple" ,line_width=1))    
#coropleth mapping india
fig_ch = px.choropleth(
                Map_IndianStatesTotal_Users_df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',                
                locations='state',
                color="Total_Transactions",                                       
                )
fig_ch.update_geos(fitbounds="locations", visible=False,)
#combining districts states and coropleth
fig_ch.add_trace( fig.data[0])
fig_ch.add_trace(fig1.data[0])
st.plotly_chart(fig_ch)
st.info('**:blue[The above India map shows the Total Transactions of PhonePe in both state wide and District wide. Please zoom in or full screen for more information]**')
