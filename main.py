#background info on https://www.sodm.nl/onderwerpen/aardbevingen.  Vanaf 1986 meet het KNMI de aardbevingen in het Groningen-gasveld. Vanaf 2014 is het KNMI-meetnetwerk aanzienlijk uitgebreid met tientallen extra sensoren en geofoons. Hiermee kunnen meer aardbevingen worden geregistreerd door het KNMI, vooral aardbevingen met een magnitude lager dan 1,5 konden voorheen minder goed worden opgemerkt door het oude netwerk. Het KNMI houdt een kaart bij met alle aardbevingen in Nederland.

from pandas.core.frame import DataFrame
import requests
import pandas as pd
import json
baseurl_tect = 'https://cdn.knmi.nl/knmi/map/page/seismologie/all_tectonic.json' 
baseurl_ind = 'https://cdn.knmi.nl/knmi/map/page/seismologie/all_induced.json' 

class apiRequest:
    def __init__(self,url):
        self.url = url
    
    def get_data(self):
        r= requests.get(self.url)
        self.data = r.json()
        return self.data

    def get_events(self, data):
        return data['events']

    def parse_json_depths(self, events):
        date_list=  []
        depth_list = []
        evaluationMode_list = []
        lat_list = []
        lon_list = []
        mag_list = []
        place_list = []
        time_list = []
        type_list = []

        for i in range(len(events)):
            date_list.append(events[i]['date'])
            depth_list.append(events[i]['depth'])
            evaluationMode_list.append(events[i]['evaluationMode'])
            lat_list.append(events[i]['lat'])
            lon_list.append(events[i]['lon'])
            mag_list.append(events[i]['mag'])
            place_list.append(events[i]['place'])
            time_list.append(events[i]['time'])
            type_list.append(events[i]['type'])
        df = pd.DataFrame(
                {'date':date_list,
                'depth':depth_list,
                'evaluationMode':evaluationMode_list,
                'lat':lat_list,
                'lon':lon_list,
                'mag':mag_list,
                'place':place_list,
                'time':time_list,
                'type':type_list})
        return df

def merge_dfs(df1, df2):
    pass
tect = apiRequest(baseurl_tect)
ind  = apiRequest(baseurl_ind)

data_ind = ind.get_data()
data_tect = tect.get_data()
events_ind = ind.get_events(data_ind)
events_tect = tect.get_events(data_tect)

df_ind = ind.parse_json_depths(events_ind)
df_tect = tect.parse_json_depths(events_tect)
print(df_ind)
#merge the dataframes
merge_df = pd.concat([df_ind, df_tect])
def convert_dtypes(df):
    for col in ['date', 'time']:
        df[col] = pd.to_datetime(df[col])
    for col in ['depth','lat', 'lon', 'mag']:
        df[col] = df[col].astype(float)
    return df

df = convert_dtypes(merge_df)
df.to_csv('df_earthquakes.csv', index=False)
