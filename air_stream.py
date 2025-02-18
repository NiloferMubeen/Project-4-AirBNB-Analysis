import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


from streamlit_option_menu import option_menu

# Background Setting

st.set_page_config(page_title = 'AirBNB',layout='wide')

st.markdown('<h1 style="text-align: center;color: #063F27;">AirBNB EDA with Python & Tableau</h1>', unsafe_allow_html=True)
st.divider()
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #02153D;
    }
</style>
""", unsafe_allow_html=True)

set_background('https://github.com/NiloferMubeen/Project-4-AirBNB-Analysis/blob/main/Bck1.png')

df1 = pd.read_csv('AirBNB.csv')

menu = option_menu("Main Menu", ["Home", 'Sample Data','Analysis and Insights','Folium Maps','Tableau Dashboard'], 
        icons=['house', 'bar-chart','graph-up-arrow','globe-americas','kanban'], menu_icon="cast", default_index=0,orientation='horizontal')

if menu == "Home":
    st.subheader("What is Airbnb Data?",divider='blue')
    with st.container():
        col1,col2 = st.columns([0.3,0.7])
        with col1:
            st.image('bnb.png')
        with col2:
            st.write("Airbnb data is information collected and stored by Airbnb, a popular online marketplace for lodging and vacation rentals.\
             This data includes details about the properties listed on the platform, such as location, amenities, availability, and pricing.\
              It also encompasses user information, such as guest reviews, host profiles. Airbnb uses this data to \
              facilitate bookings, improve user experience, and make informed business decisions.\
              Examples of Airbnb data include information about listings,reviews, host profiles, and pricing")
            st.markdown("<h4 style='text-align: left; color: #063F27;'>What are the attributes of AirBnB Data? </h4>", unsafe_allow_html=True)
            st.write("There are many different aspects to AirBnB data from both the consumer and host side of the operation.")
            st.markdown("<h5 style='text-align: left; color: #063F27;'>Consumer-side data: </h5>", unsafe_allow_html=True)
            st.write("This can include user-generated content like reviews and experiences shared in forums. \
                      More basic data includes average duration rate.")
            st.markdown("<h5 style='text-align: left; color: #063F27;'>Host-side data: </h5>", unsafe_allow_html=True)
            st.write("This includes property availabilities, property size and features as well as nightly rates.")
if menu == 'Sample Data':
            st.dataframe(df1.head(),hide_index = True)

if menu == 'Analysis and Insights':
            option = st.selectbox(
            'Select an option',
            ('Top 10 Suburbs by listings', 'Listings by Room type', 'Listings by Property Type',
            'Guests per booking','Average cost for different property types','Top 5 Hosts','Reviews vs Price'))
            st.write('You selected:', option)

            if option == 'Top 10 Suburbs by listings':
                               
                        s = df1['neighbourhood'].value_counts().sort_values(ascending=True)
                        s = s[-10:]
                        sub = pd.DataFrame(s, columns=['count'])
                        fig = px.bar(sub, x="count", y=sub.index,color_discrete_sequence=px.colors.sequential.Viridis,orientation='h')
                        st.plotly_chart(fig, use_container_width=True)                          
            if option == 'Listings by Room type':
                        c1,c2 =st.columns([0.6,0.4])
                        with c1:
                              r = df1['room_type'].value_counts().sort_values(ascending=True)
                              rmty = pd.DataFrame(r, columns=['count'])
                              fig = px.bar(rmty, x="count", y=rmty.index,color_discrete_sequence=px.colors.sequential.Cividis,orientation='h')
                              st.plotly_chart(fig, use_container_width=True)  
                         
                        with c2:
                                    
                            st.markdown("<h5 style='text-align: left; color: #063F27;'>Observation: </h5>", unsafe_allow_html=True)
                            st.divider()
                            st.markdown("<h6 style='text-align: left; color: #black;'>Here,the entire home/apt’s listings is aproximately twice that of private \
                                            rooms. Home/Apts are usually rented on a monthly basis. According to the data, Per day rent of the rooms are costlier as compared to month’s \
                                            rent. So renting the Private rooms can help the owners earn more as compared to renting an\
                                            entire apartment/home </h6>", unsafe_allow_html=True)
            if option == 'Listings by Property Type':
                  p = df1['Property_type'].value_counts().sort_values(ascending=True)
                  prop = pd.DataFrame(p,columns= ['count'])
                  fig = px.bar(prop, x="count", y=prop.index,color_discrete_sequence=px.colors.sequential.Rainbow,orientation='h')
                  st.plotly_chart(fig, use_container_width=True)    
            if option == 'Guests per booking':
                  a1,a2 = st.columns([0.7,0.3])
                  with a1:
                        a = df1['Accomadates'].value_counts().sort_index()
                        acc = pd.DataFrame(a, columns=['count'])
                        fig = px.bar(acc, x= acc.index, y = 'count',color_discrete_sequence=px.colors.sequential.RdBu,orientation='v')
                        st.plotly_chart(fig, use_container_width=True) 
                  with a2:
                        st.markdown("<h5 style='text-align: left; color: #063F27;'>Observation: </h5>", unsafe_allow_html=True)
                        st.divider()
                        st.markdown("<h6 style='text-align: left; color: #black;'>From the plot we can observe, about 70% of bookings are 2 to 4\
                                     guests per property. Probably it’s a single room apartment or a hotel, which means people \
                                    mostly prefer single room apartments/Private rooms/Shared rooms. Thus instead of renting out\
                                     an entire apt/home, renting rooms can attarct more customers.  </h6>", unsafe_allow_html=True)
            if option == 'Average cost for different property types':
                  room = df1.groupby(['Property_type','Country'])['Price'].mean().reset_index()
                  room = df1.sort_values('Price',ascending=False)
                  st.table(room[['Property_type','Country','Price']].head())
            if option == 'Top 5 Hosts':
                  host_stat = df1.groupby(['host_name','verified_host']).agg({
                                                                'host_id': 'count',
                                                                'Price': 'mean',
                                                                 'min_nights': 'mean',
                                                                 'review_score': 'mean'
                                                                                })
                  host_stat = host_stat.rename(columns={'host_id': 'listings_count', 'Price': 'mean_price', 'min_nights': 'mean_minimum nights'}).reset_index()
                  st.dataframe(host_stat.sort_values(by='listings_count',ascending=False).head(5),hide_index=True)
            if option == 'Reviews vs Price':
                  b1,b2 = st.columns(2)
                  with b1:
                        fig = px.scatter(df1, x="Price", y="review_score",color = 'Property_type',size='Accomadates')
                        st.plotly_chart(fig, use_container_width=True)    
                  with b2:
                        st.markdown("<h5 style='text-align: left; color: #063F27;'>Observation: </h5>", unsafe_allow_html=True)
                        st.divider()
                        st.markdown("<h6 style='text-align: left; color: #black;'>From the plot, It seems price also leads to a high review score.\
                                     Here most of the listings with a price range of 10-3000 has a very high review score. Also, there are few\
                                    cheap listings with a low review rating.</h6>", unsafe_allow_html=True)
                        
if menu == 'Folium Maps':
    st.subheader("Folium Choropleth")
    st.divider()
    st.markdown("<h4 style='text-align: center; color: #063F27;'>Property prices across the continents </h4>", unsafe_allow_html=True)
    st.image('airbnb_choropleth.png')
    st.subheader("Folium Marker Map")
    st.divider()
    st.markdown("<h4 style='text-align: center; color: #063F27;'>Airbnb listings across the continents </h4>", unsafe_allow_html=True)
    st.image('airbnb_folium.png')
if menu == 'Tableau Dashboard':
    st.image('AirbnbTBW.png')
