import streamlit as st
import requests
import numpy as np
import pandas as pd
import plotly.express as px


st.title('College Football Recruiting')
st.markdown('_Stats courtesy of @CFB_Data_')

@st.cache
def Data():
    response = requests.get(
        'https://api.collegefootballdata.com/coaches',
        )

    coaches = pd.io.json.json_normalize(response.json())

    data = pd.DataFrame()

    for i in coaches.index:
        df = pd.DataFrame(coaches['seasons'][i])
        df['coach'] = coaches['first_name'][i] + ' ' + coaches['last_name'][i]
        data = pd.concat([data,df])

    data = data[['school','coach','year']]
    
#change in future to handle 2020 unknown
    data = data.query("year > 1999 and year <2020")
   
    data.rename(columns={"school": "team"}, inplace = True)

    data = data
    response = requests.get(
    'https://api.collegefootballdata.com/recruiting/teams',
    )

    recruiting  = pd.read_json(response.text)

    data = data.merge(recruiting, how = 'right', on = ['year','team'] ).sort_values(by = ['year','team'])

    teams = list(list(data.sort_values(by='team')['team'].unique()))

    coaches = list(list(data.sort_values(by='coach')['coach'].unique()))

#groupby.transform to get average for coach and average for team


    return [data, teams, coaches]



df, teams, coaches = Data()



selectTeams = st.multiselect(
    "Choose teams",teams, ["Alabama", "Florida State"]
)

selectCoaches = st.multiselect(
    "Choose coaches",coaches, ["Nick Saban", "Mike Norvell"]
)
if not (selectCoaches or selectTeams):
    st.error("Please select at least one filter.")


df = df.query(("team in @selectTeams or coach in @selectCoaches"))

#checkbox for if you want to divide by coach or not
#Change to an unknown groupby max min (i.e. Unknown
#df['coach'] = df['coach'].fillna('Unknown')
df = df[~df['coach'].isna()]

#df['unique'] = df['coach'] + ' - ' + df['team']

if len(selectTeams) < 2:
    fig = px.line(df, x="year", y="points", color = 'coach',hover_name="coach", text = "coach", line_group = 'team', line_dash = 'coach')
   #fig = px.line(df, x="year", y="points", color = 'team',hover_name="coach", line_group = 'team', title = ', '.join(selectCoaches) + ' Recruiting')
else:
    fig = px.line(df, x="year", y="points", color = 'team')

fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig.update_traces(textposition='top left')

fig.update_xaxes(showline=True, linewidth=.5, linecolor='grey')
fig.update_yaxes(showline=True, linewidth=.5, linecolor='grey')


fig

