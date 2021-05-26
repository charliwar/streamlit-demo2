#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st




st.title('College Football Recruiting Pipelines')
st.markdown('_Data courtesy of @CFB_Data | Original idea by @ConorMcQ5_')


#read-in data that was collected from collegefootballdata.com
#cache this function so that streamlit doesn't rerun it everytime a user input is changed
@st.cache(allow_output_mutation=True)
def getData():
    #read in
    recruits = pd.read_csv(r'https://raw.githubusercontent.com/BenDavis71/CFB-Recruiting/master/recruits.csv') 
    teams = pd.read_csv('https://raw.githubusercontent.com/BenDavis71/CFB-Recruiting/master/teams.csv', index_col='school')

    #force the logo string to behave as a list
    teams['logos'] = teams['logos'].apply(lambda x: eval(x))

    #generate list of teams from dataframe
    teamsList = teams.index.tolist()
    return recruits, teams, teamsList 


recruits, teams, teamsList = getData()


#user input for date range
years = st.slider("Date Range", min_value=2000, max_value=2020, value=(2000, 2020))

#user input for recruit type
blueChips = st.radio('Blue Chip Filter', ['Blue Chips Only','All Recruits'], index = 1)
blueString = ''

#user input for team
school = st.selectbox("Team", teamsList, index = teamsList.index('Florida State'))


#filter recruiting dataframe to match user selections
recruits = recruits[recruits['committedTo'] == school]
recruits = recruits[recruits['year'].between(years[0],years[1])]
if blueChips == 'Blue Chips Only':
    recruits = recruits[recruits['stars'] >= 4]
    blueString = 'Blue Chip '


#get school relevant presentation info
info = teams.loc[school]
color, gradientColor,logo = info[1:]
logo = logo[0]

#groupby states for the remaining rows in order to correctly format the dataframe for map-making
states = recruits[['stateProvince','name']].groupby('stateProvince', as_index = False).count()



#create map and define colors
fig = go.Figure(data=go.Choropleth(
    locations=states['stateProvince'],
    z = states['name'],
    locationmode = 'USA-states',
    colorscale = [[0, gradientColor],[1.0, color]],
    marker_line_color='white'
))

#update title and map scope
fig.update_layout(
    title_text = f'{school} {blueString}Recruiting, {years[0]}-{years[1]}',
    title_x=0.5,
    title_y=0.9,
    font=dict(
    family='Arial',
    size=20,
    ),
    geo_scope='usa',
    
)

#add logo
fig.add_layout_image(
    dict(
        source=logo,
        xref="paper", yref="paper",
        x=.95, y=.1,
        sizex=0.25, sizey=0.25,
        xanchor="right", yanchor="bottom"
    )
)

st.write(fig)

st.markdown('___')
st.markdown('Created by [Ben Davis](https://github.com/BenDavis71/)')
