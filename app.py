import streamlit as st
import joblib
import pandas as pd
import numpy as np
from pandas import read_csv
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

hide_menu = """
<style>
footer:after{
    content: 'Copyright @ 2022: Simisola Olagunju' ;
    display:block;
    position:relative;
    color:tomato;
    padding:5px;
    top:3px
}
<style>
"""
st.markdown(hide_menu,unsafe_allow_html=True)
loaded_model = joblib.load('reg2.sav')

# Create a page dropdown
st.sidebar.header('Welcome')
page = st.sidebar.selectbox("""
Make your selection""", ["Main Page", "Data Visualisation", "Data Prediction"])


if page == "Main Page":

    ### INFO
    st.title('Carbon Emissions Prediction App')
    st.markdown("""---""")
    st.write(
        '''
        This prediction app is used to predict the per capita emission in the UK.
        ''')
    image = Image.open('climate.jpg')
    st.image(image, caption='Carbon emission sources')
    st.markdown("""---""")
    st.write(
        '''
        It is undeniable that human activity has warmed the atmosphere, oceans, and land, according to the most recent assessment 
        from the Intergovernmental Panel on Climate Change (IPCC) in August 2021. Additionally,climate change happens more quickly 
        than initially assumed. According to the most recent estimates, human impact caused a rise in the average global surface temperature
         of 1.07°C from 2010 to 2019 compared to 1850 to 1900. AI has a great potential to lower carbon emissions by making forecasts that are more 
         accurate or by streamlining operations across various industries. AI can be used, for instance, to manage supply networks, forecast 
         extreme weather, or keep an eye on peatlands.
        ''')
    st.markdown("""---""")
    st.write(
        '''
        # Data Description
        ''')
    # data description
    col1, col2 = st.columns(2)

    button1 = col1.button("features")
    if (button1):
        st.write('**Region/Country** - regions in the UK where the data was collected')
        st.write('**Year** - year of CO2 emission collection')
        st.write('**Industry_Total** - total CO2 emissions for industry electrity, gas, other fuels, large indusrial installations and agriculture')
        st.write('**Commercial_Total** - total CO2 emissions for commercial electricity, gas and other fuels')
        st.write('**Public_Sector_Total** - total CO2 emissions for public sector electricity, gas and other fuels')
        st.write('**Domestic_Total** - total CO2 emissions for domestic electricity, ags and other fuels')
        st.write('**Transport_Total** - total CO2 emissions for diesel railways, road transport A roads, motorways, minor roads and other forms of transport')
        st.write('**LULUCF_Net_Emissions** -(land use, land use chane and foresrtry) total CO2 emissions for net emissions in forestland, grassland, wetlands, cropland, settlements and harvested wood products ')
        st.write('**Population** - population of each region where the data was collected in thousands')
        st.write('**Area(km2)** - area covered for each region for data collection')
        st.write('**Emission per km2(kt)** - total emission for each square km')

    button2 = col2.button("Target Variable")
    if (button2):
        st.write('**Per_Capita_Emissions(t)** - tonnes of CO2 emission per person')

if page == "Data Visualisation":

    ### INFO
    st.title('Data Visualization')

    @st.cache
    def load_data():
        my_data = read_csv('COM726.csv')

        # Drop rows which have all NaN in its row
        my_data = my_data.dropna(how='all')

        # Drop columns
        my_data = my_data.drop(['Second_Tier_Authority', 'Local_Authority', 'Code', 'Unnamed: 16', 'Grand_Total'],
                               axis=1)
        return my_data

    my_data = load_data()
    st.write(
        """
        ### Number of Data from Different Region/Country
        """
    )
    data = my_data['Region_Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct='%1.2f%%', shadow= True, startangle= 90)
    ax1.axis('equal')
    st.pyplot(fig1)

    st.markdown("""---""")
    st.write(
        """
        ### Mean Per Capita Emission based on Country/Region
        """
    )
    data =my_data.groupby(['Region_Country'])['Per_Capita_Emissions(t)'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.markdown("""---""")
    st.write(
        """
        ### Mean Per Capita Emission based on Year
        """
    )
    fig = plt.figure(figsize=(15, 8))
    sns.lineplot(x='Year', y='Per_Capita_Emissions(t)', data=my_data, linewidth=2.5)
    st.pyplot(fig)

if page == "Data Prediction":

    ### INFO
    st.title('Carbon Emissions Prediction')
    region = ('North East',
    'North West',
    'Yorkshire and the Humber',
    'East Midlands',
    'West Midlands',
    'East of England',
    'London',
    'South East',
    'South West',
    'Wales Scotland',
    'Northern Ireland')
    country = st.selectbox('Country/Region', region)
    #FUNCTION
    def user_report():
        Year = st.slider('Year', 2000,2050)
        Industry_Total = st.number_input('Industry Total', key=0)
        Commercial_Total = st.number_input('Commercial Total', key=1)
        Public_Sector_Total = st.number_input('Public Sector Total', key=2)
        Domestic_Total = st.number_input('Domestic Total', key=3)
        Transport_Total = st.number_input('Transport Total', key=4)
        LULUCF_Net_Emissions = st.number_input('LULUCF Net Emission', key=5)
        Population = st.number_input('Population', key=6)
        Area = st.number_input('Area(km2)', key=7)
        Emissions_per_km2 = st.number_input('Emission per km2(kt)', key=8)

        user_report_data = {
            'Year': Year,
            'Industry_Total': Industry_Total,
            'Commercial_Total': Commercial_Total,
            'Public_Sector_Total': Public_Sector_Total,
            'Domestic_Total': Domestic_Total,
            'Transport_Total': Transport_Total,
            'LULUCF_Net_Emissions': LULUCF_Net_Emissions,
            'Population': Population,
            'Area' : Area,
            'Emissions_per_km2' : Emissions_per_km2
        }

        report_data = pd.DataFrame(user_report_data, index=[0])
        return report_data

    user_data = user_report()
    st.header(' carbon Emission Data')
    st.write(user_data)

    emission = loaded_model.predict(user_data)
    ok = st.button('Predict Emission')
    if ok:
        st.subheader(f'The Estimated Per Capita Emission is {np.round(emission[0], 2)}')

#st.write("Made by: Simisola Olagunju 💛")


