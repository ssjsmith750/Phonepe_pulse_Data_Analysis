import pandas as pd 
import plotly.express as px
import streamlit as st 
import mysql.connector
import plotly.graph_objects as go
#import matplotlib as plt
# Database Connection
PhonePe=mysql.connector.connect(host='localhost',
                        database='phonepe',
                        user='root',
                        password='**********')
mycursor = PhonePe.cursor()
st.title('PhonePe Pulse and User Data Analysis(2018-2022):signal_strength:')
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

Year = st.selectbox(
    'Please select the Year',
    ('2018', '2019', '2020','2021','2022'))
Quarter = st.selectbox(
    'Please select the Quarter',
    ('1', '2', '3','4'))
state = st.selectbox(
    'Please select the State',
    ('india','andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
       'assam', 'bihar', 'chandigarh', 'chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
       'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
       'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
       'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
       'uttarakhand', 'west-bengal'))
year=int(Year)
quarter=int(Quarter)
State = str(state)

Districtwise_MapTransaction=Map_Transaction_Table_df.loc[(Map_Transaction_Table_df['Year'] == year ) & (Map_Transaction_Table_df['Quarter']==quarter) ].copy()
Statewise_Transaction=Districtwise_MapTransaction[Districtwise_MapTransaction["State"] == "india"]
Districtwise_MapTransaction.drop(Districtwise_MapTransaction.index[(Districtwise_MapTransaction["State"] == "india")],axis=0,inplace=True)
# Dynamic Scattergeo Data Generation
Districtwise_MapTransaction = Districtwise_MapTransaction.sort_values(by=['Locations'], ascending=False)
Districts_GeoLocation = Districts_GeoLocation.sort_values(by=['District'], ascending=False) 
Total_Amount=[]
for i in Districtwise_MapTransaction['Total_Amount']:
    Total_Amount.append(i)
Districts_GeoLocation['Total_Amount']=Total_Amount
Total_Transaction=[]
for i in Districtwise_MapTransaction ['Total_Transactions_Locationwise']:
    Total_Transaction.append(i)
Districts_GeoLocation['Total_Transactions']=Total_Transaction
Districts_GeoLocation['Year_Quarter']=str(year)+'-Q'+str(quarter)
# Dynamic Coropleth
Map_IndianStatesTotal_Users_df = Map_IndianStatesTotal_Users_df.sort_values(by=['State'], ascending=False)
Statewise_Transaction = Statewise_Transaction.sort_values(by=['Locations'], ascending=False)
Total_Amount=[]
for i in Statewise_Transaction['Total_Amount']:
    Total_Amount.append(i)
Map_IndianStatesTotal_Users_df['Total_Amount']=Total_Amount
Total_Transaction=[]
for i in Statewise_Transaction['Total_Transactions_Locationwise']:
    Total_Transaction.append(i)
Map_IndianStatesTotal_Users_df['Total_Transactions']=Total_Transaction
"*****************************************MAP********************************************"

State_Geo_Location_Data_df = State_Geo_Location_Data_df.sort_values(by=['state'], ascending=False)
State_Geo_Location_Data_df['Registered_Users']=Map_IndianStatesTotal_Users_df['Registered_Users']
State_Geo_Location_Data_df['Total_Amount']=Map_IndianStatesTotal_Users_df['Total_Amount']
State_Geo_Location_Data_df['Total_Transactions']=Map_IndianStatesTotal_Users_df['Total_Transactions']
State_Geo_Location_Data_df['Year_Quarter']=str(year)+'-Q'+str(quarter)
fig=px.scatter_geo(State_Geo_Location_Data_df,
                   lon=State_Geo_Location_Data_df['Longitude'],
                   lat=State_Geo_Location_Data_df['Latitude'],                                
                   text = State_Geo_Location_Data_df['code'], 
                   hover_name="Total_Transactions", 
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
             
                   hover_name="District", 
                   hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                   title='District',
                   size_max=33,
                   #animation_frame='Total_Transactions',
                   #projection='kavrayskiy7',
                   )

fig1.update_traces(marker=dict(color=(0, 12) ,line_width=1))
 
#ax = plt.axes(projection ='3d')
#coropleth mapping india
fig_ch = px.choropleth(
                Map_IndianStatesTotal_Users_df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',                
                locations='State',
                color="Total_Transactions",                                       
                )
fig_ch.update_geos(fitbounds="locations", visible=False,)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})  
#combining districts states and coropleth
fig_ch.add_trace( fig.data[0])
fig_ch.add_trace(fig1.data[0])
st.plotly_chart(fig_ch)
st.info('**:blue[The above India map shows the Total Transactions of PhonePe in both state wide and District wide.]**')


#####################################################  MAP ########################################################

st.write('# :orange[USERS DATA ANALYSIS ]')
st.write('### :orange[Mobile Brands] ')
state = st.selectbox(
    'Please select the State',
    ('india','andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
       'assam', 'bihar', 'chandigarh', 'chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
       'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
       'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
       'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
       'uttarakhand', 'west-bengal'),key='Z')
Y = st.selectbox(
    'Please select the Year',
    ('2018', '2019', '2020','2021','2022'),key='X')
y=int(Y)
s=state
brand=Aggregated_User_df[Aggregated_User_df['Year']==y] 
brand=Aggregated_User_df.loc[(Aggregated_User_df['Year'] == y) & (Aggregated_User_df['State'] ==s)]
myb= brand['Mobile_Model_Name'].unique()
x = sorted(myb)
b=brand.groupby('Mobile_Model_Name').sum()
b['brand']=x
br=b['Registered_Users'].sum()
labels = b['brand']
values = b['Registered_Users']
fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4,customdata=labels,textinfo='label+percent',texttemplate='%{label}<br>%{percent:1%f}',insidetextorientation='horizontal',textfont=dict(color='#000000'),marker_colors=px.colors.qualitative.Dark24)])
st.plotly_chart(fig3)
st.info('**:orange[The above donut Graph shows how the users are registered through different brand in india. which brand has more users and less users  ]**')
