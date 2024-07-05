import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from PIL import Image
from datetime import datetime, date

# Setting page configuration
st.set_page_config(page_title="Kiva dashboard", page_icon="💹", layout='wide')

# Loading data
kiva_loans = pd.read_csv('cleaned_kivaloans.csv')
partners = pd.read_csv('loan_themes_by_region.csv')

# Define an initial data variable to hold the entire kiva_loans DataFrame
data = kiva_loans

with st.sidebar:
    
    st.sidebar.image('Kiva.org_logo_2016.png')
    st.sidebar.subheader("This dashboard for Kiva.org will help to estimate the poverty levels of residents in the regions where Kiva has active loans")
    st.sidebar.write("")
    country = st.sidebar.selectbox("Country", ['All'] + list(kiva_loans['country'].unique()))
    # data after country selection
    if country != 'All':
        data = data[data['country'] == country]
    sector = st.sidebar.selectbox("Sector", ['All'] + list(data['sector'].unique()))
    # data after country and sector selection
    if sector != 'All':
        data = data[data['sector'] == sector]
    activity = st.sidebar.selectbox("Activity", ['All'] + list(data['activity'].unique()))
    # data after country and sector and activity selection
    if activity != 'All':
        data = data[data['activity'] == activity]
    gender = st.sidebar.selectbox("Gender", ['All'] + list(data['borrower_genders'].unique()))
    # data after country and sector and activity and gender selection
    if gender != 'All':
        data = data[data['borrower_genders'] == gender]
    repay = st.sidebar.selectbox("Repayment Method", ['All'] + list(data['repayment_interval'].unique()))

    kiva_loans['disbursed_time'] = pd.to_datetime(kiva_loans['disbursed_time'])

    # Add a slider for disbursed time
    start_date = kiva_loans['disbursed_time'].min().date()
    end_date = kiva_loans['disbursed_time'].max().date()
    selected_start_date = st.sidebar.slider('Select start date', start_date, end_date, start_date)
    selected_end_date = st.sidebar.slider('Select end date', selected_start_date, end_date, end_date)

    st.sidebar.write("")
    st.sidebar.markdown("Made by Omayma Ali")


# Remove whitespace from the top of the page and sidebar
# sidebar background color
st.markdown("""
    <style>
    .block-container {
        padding-top: 4rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 1rem;
        }
    [data-testid=stSidebar] {
        background: linear-gradient(to bottom left, #999966 0%, #ccffff 37%);
        } 
    [data-testid="metric-container"] {
        border: 1px solid #e6e6ff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }   
    [data-testid="stMetricLabel"] {
        font-family: Georgia, serif;
        color:rgb(0, 0, 153);
        font-weight: bold;
        font-size: 30px;
        }
    [data-testid="stImage"]{
        border: 1px solid #e6e6ff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);    
        }
    [data-testid="caption"] {
        font-family: Georgia, serif;
        color:#288BA8;
        font-weight: bold;
        font-size: 14px;
        }  
    [data-testid="stMarkdownContainer"]{
        font-family: Georgia, serif;
        color:#009933;
        font-weight: bold;
        font-size: 35px;   
        }

    </style>
""", unsafe_allow_html=True)
    
# Information Cards
card1, card2, card3, card4 = st.columns((3,3,2,2))

# filtering Function
def filter(country, sector, activity, gender, repay, selected_start_date, selected_end_date):
    if country == 'All' and sector == 'All' and activity == 'All' and gender == 'All' and repay == 'All':
        filtered_loans = kiva_loans.copy()
    else:
        filtered_loans = kiva_loans

        if country != 'All':
            filtered_loans = filtered_loans[filtered_loans['country'] == country]

        if sector != 'All':
            filtered_loans = filtered_loans[filtered_loans['sector'] == sector]

        if activity != 'All':
            filtered_loans = filtered_loans[filtered_loans['activity'] == activity]

        if gender != 'All':
            filtered_loans = filtered_loans[filtered_loans['borrower_genders'] == gender]

        if repay != 'All':
            filtered_loans = filtered_loans[filtered_loans['repayment_interval'] == repay]
    
    filtered_loans = filtered_loans[(filtered_loans['disbursed_time'].dt.date >= selected_start_date) &\
                     (filtered_loans['disbursed_time'].dt.date <= selected_end_date)]
  
    return filtered_loans

# Filtered DataFrame
filtered_loans = filter(country, sector, activity, gender, repay, selected_start_date,selected_end_date)

# Cards Values
funded = filtered_loans['funded_amount'].sum()
loan = filtered_loans['loan_amount'].sum()
lender = filtered_loans['lender_count'].sum()
borrower = filtered_loans['borrower_count'].sum()

# Show The Cards
card1.metric("Total Funded Amount", f"${funded}")
card2.metric("Total Loan Amount", f"${loan}")
card3.metric("Total Lender Count", f"{lender}")
card4.metric("Total Borrower Count", f"{borrower}")

    
# Charts Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Kiva Work", "Countries", "Partners", "Time"])

# About Kiva Work Tab
with tab1:
    
    #opening the image
    graphic_raim = Image.open('graphic_raim.webp')
    graphic_margarita = Image.open('graphic_margarita.webp')
    im1 = Image.open('1.webp')
    im2 = Image.open('2.webp')
    im3 = Image.open('3.webp')
    im4 = Image.open('4.webp')

    # Header to Show How funded in kiva is simple    
    # st.subheader('From a new fishing net to community solar power, it’s easy to help fund a loan that changes someone’s life.')

    # Images2 Cards for Kiva funded stages
    img1, img2, img3, img4 = st.columns(4)
    # Display the images in the columns
    img1.image(im1, 
               caption='Find a person you want to support')
    img2.image(im2, 
               caption='Decide how much you want to contribute')
    img3.image(im3, 
               caption='Check out—your funds are allocated to the borrower')
    img4.image(im4, 
               caption='Get repaid, and lend to someone else!')

    # Images Cards for borrower
    img5, img6 = st.columns(2)
    # Display the images in the columns
    img5.image(graphic_raim)
    img6.image(graphic_margarita)

# Country visuals    
with tab2:

    visual1, visual2 = st.columns((6,4))
    with visual1:
        st.subheader('Total Country Loan Amount Per Year')
        filtered_loans['posted_time'] = pd.to_datetime(filtered_loans['posted_time'])
        filtered_loans['year']=filtered_loans['posted_time'].dt.year
        # Create the line plot using Plotly Express
        fig = px.line(filtered_loans, 
                      x='year', 
                      y='funded_amount', 
                      color='activity')
        # Customize x-axis and y-axis labels
        fig.update_xaxes(title='Year')
        fig.update_yaxes(title='Loan Amount')
        # Set the x-axis tick format to display only the year
        #fig.update_layout(xaxis=dict(tickformat='%Y'))
        st.plotly_chart(fig, use_container_width=True)

    with visual2:
        st.subheader('The Most Regions Borrowed')
        most_region = filtered_loans.groupby(['region'])['loan_amount'].sum().sort_values(ascending=False).head()
        fig = px.pie(data_frame=most_region, 
                     names=most_region.index, 
                     values=most_region.values, 
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)


    visual3, visual4 = st.columns((4,6))
    with visual3:
        st.subheader('Lender Count For Each Region')
        region_lender = filtered_loans.groupby(['region'])['lender_count'].sum().sort_values(ascending=False).head()
        fig = px.pie(region_lender, 
                     names=region_lender.index, 
                     values=region_lender.values, 
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with visual4:
        st.subheader('Country Regions')
        Regions_count = filtered_loans['region'].value_counts().sort_values(ascending=False).head(15)
        fig = px.bar(Regions_count, 
                     x=Regions_count.index, 
                     y=Regions_count.values, 
                     color=Regions_count.values)
         # Customize x-axis and y-axis labels
        fig.update_xaxes(title='Region')
        fig.update_yaxes(title='Count')
        st.plotly_chart(fig, use_container_width=True)     
 
 
#Partners visuals    
with tab3:

    visual1, visual2 = st.columns(2)
    with visual1:
        st.subheader('Top Partners Names')
        most_partner_loans = filtered_loans.groupby('partner_id')['loan_amount'].sum().sort_values(ascending=False).head()
        most_partners = filtered_loans['partner_id'].value_counts().sort_values(ascending=False).head()

        partner_ids = partners[(partners['Partner ID'].isin(most_partner_loans.index)) | (partners['Partner ID']\
                                                                                          .isin(most_partners.index))]['Partner ID']
        # Filter partner names based on partner IDs
        partner_names = partners[partners['Partner ID'].isin(partner_ids)][['Partner ID', 'Field Partner Name']]

        # Create a pivot table with the first partner name value for each partner ID
        pivot_table = partner_names.groupby('Partner ID').first().reset_index()

        # Filter pivot table based on most_partner_loans and most_partners indices
        filtered_table = pivot_table[pivot_table['Partner ID'].isin(most_partner_loans.index) | pivot_table['Partner ID']\
                                     .isin(most_partners.index)]
        st.dataframe(filtered_table)


    with visual2:
        st.subheader('Lender Count VS Loan Amount')
        fig = px.scatter(filtered_loans,
                         x='lender_count',
                         y='loan_amount',
                         color='borrower_genders',
                         size='funded_amount')
        # Customize x-axis and y-axis labels
        fig.update_xaxes(title='Lender Count')
        fig.update_yaxes(title='Loan Amount')
        st.plotly_chart(fig, use_container_width=True)

    visual3, visual4 = st.columns(2)
    with visual3:
        st.subheader('Top Partners ')     
        fig = px.bar(most_partners,
                        x=most_partners.index,
                        y=most_partners.values,
                        color=most_partners.values)
        # Customize x-axis and y-axis labels
        fig.update_xaxes(title='Partner')
        fig.update_yaxes(title='Loans Count')
        st.plotly_chart(fig, use_container_width=True)

    with visual4:
        st.subheader('Top Partners Total Loans')
        fig = px.pie(most_partner_loans,
                    names=most_partner_loans.index, 
                    values=most_partner_loans.values,
                    hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
 
# Time tab
with tab4:
    
    # Create the line plot for loan_amount
    fig = px.line(filtered_loans,
                   x='disbursed_date',
                   y='loan_amount', 
                   labels='Loan', 
                   )
    # Customize x-axis and y-axis labels
    fig.update_xaxes(title='Disbursed Date')
    fig.update_yaxes(title='Loan Amount')
     # Set the x-axis tick format to display only the year
    #fig.update_layout(xaxis=dict(tickformat='%Y'))
    # Display the line plot
    st.plotly_chart(fig, use_container_width=True)

    # Create the line plot for funded_amount
    fig = px.line(filtered_loans, 
                  x='disbursed_date', 
                  y='funded_amount', 
                  labels='funded', 
                  )
    # Customize x-axis and y-axis labels
    fig.update_xaxes(title='Disbursed Date')
    fig.update_yaxes(title='Funded Amount')
    # Set the x-axis tick format to display only the year
    #fig.update_layout(xaxis=dict(tickformat='%Y'))
    # Display the line plot
    st.plotly_chart(fig, use_container_width=True)



