# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 19:51:08 2020

@author: sanja
"""



import pandas as pd
import numpy as np
import re
import datetime
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

import plotly.graph_objects as go
import plotly.express as px

import dash_bootstrap_components as dbc
import dash_table as dt

# Global variables

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) # [dbc.themes.BOOTSTRAP]
project_name = None

# All Function would be defined here

#  Function to seperate the date and time from column 9

def datetime_divider(data):

    for index in range (len(data)):

        if (re.match("^\d",str(data[index]))):

            regex = re.compile("\d{1,8}")

            a = regex.findall(str(data[index]))

            print(a)

            data[index ] = [ a[0] , a[1] ]

        else:

            data[index ] = [np.nan, np.nan]
    return data

# Function to convert the data in desired date format

def date_modifier(data):

    # data type of data is list

    # 20190620 should be converted to 2019-06-20

    for index in range(len(data)):

        if re.match("^\d", str(data[index])):

            year = str(data[index][:4])

            month = str(data[index][4:6])

            day = str(data[index][6:])

            data[index] = "-".join([year, month, day])

        else:

            data[index] =  np.nan
    return data

# Function to convert the data in desired datetime format

def time_modifier(data):

    # Data type of data is list

    # 032717 should be converted into 03:27:17 AM

    for index in range(len(data)):

        data[index] = str(data[index])

        

        if re.match("^\d", data[index]):

            m = int(data[index][:2])

            mi = data[index][2:4]

            sec = data[index][4:]

            

            if m >=12:

                if m == 12:

                    hr = str(m)

                else:

                    hr = str(m-12)

                merd = "PM"

            else:

                if m == 0:

                    hr = str(12)

                else:

                    hr = data[index][:2]

                merd = "AM"

            

            data[index] = ":".join([hr, mi, sec]) + " " + merd

        else:

            data[index] = np.nan

    return data

def replace_simple_with_Standard_terminology(dataset):

    # This part replace the data with standard terminologies in col 5, 267, 312

    # Replacing String in the columns with standard Terminology

    dataset[5] = dataset[5].replace("Originating", "Outgoing")

    dataset[5] = dataset[5].replace("Terminating", "Incoming")

    

    dataset[267] = dataset[267].replace("Success", "Voice Portal")
    dataset[312] = dataset[312].replace("Shared Call Appearance", "Secondary Device")

    return dataset

def remove_Unwanted_data(data):

    # data type of data is list

    for index in range(len(data)):

        if data[index] == "Secondary Device" or data[index] =="Primary Device":

            continue

        else:

            data[index] = np.nan 

    return data

# This part sets all the services in one column 147

def combine_All_Services(data1, data2, data3):
    for index in range(len(data1)):

        if data1[index] is np.nan:

            

            if data2[index] is not np.nan and data3[index] is not np.nan:

                data1[index] = str(data2[index])+ "," + str(data3[index])

            

            elif data2[index] is not np.nan:

                data1[index] = data2[index]

            

            else:

                data1[index] = data3[index]

            

        else:

            continue

    return data1

    
# Convert data into a specific format

def call_time_fetcher(data):
    for index in range(len(data)):

        data[index] = str(data[index])

        if data[index]!="nan":

            year = data[index][:4]

            month = data[index][4:6]

            day = data[index][6:8]

            hours = data[index][8:10]

            minutes = data[index][10:12]

            seconds = str(round(float(data[index][12:])))

            if int(seconds) >= 60:

                seconds = int(seconds) -60

                minutes = int(minutes)+1 

            if int(minutes) >=60:

                hours = int(hours)+1

                minutes  = int(minutes) - 60 

            data[index] = f"{year}-{month}-{day} {hours}:{minutes}:{seconds}"

        else:

            data[index] = np.nan

    return data

def hourly_range(data):

    for index in range(len(data)):

        data[index] = str(data[index])

        if data[index]!="nan":

            if re.search("PM", data[index]):

                time_data =  re.findall("\d+", data[index])

                if time_data[0] != "12":

                    time_data = int(time_data[0]) + 12

                else:

                    time_data = time_data[0]

                

            else:

                time_data =  re.findall("\d+", data[index])

                if int(time_data[0]) == 12:

                    time_data = f"0{int(time_data[0]) - 12}"

                else:

                    time_data = time_data[0]

                

                

            data[index] = f"{time_data}:00 - {time_data}:59"

        else:

            data[index] = np.nan

    return data

def weekly_range(data):

    for index in range(len(data)):

        data[index] = str(data[index])

        if data[index]!="nan":

            yr, mon, day = [int(x) for x in data[index].split("-")]

            ans = datetime.date(yr, mon, day)

            data[index] = ans.strftime("%A")

        else:

            data[index] = np.nan

    return data

def load_data():

    # We need to write the logic of loading the data

    print("Start of the load_data function")
    # variables by default are local variables

    call_dataset_name = 'Forsk_Internship_Batch_6/CDR Dataset/Call_data.csv'

    service_dataset_name = 'Forsk_Internship_Batch_6/CDR Dataset/Service_data.csv'

    device_dataset_name = 'Forsk_Internship_Batch_6/CDR Dataset/Device_data.csv'

    

    global call_data

    call_data = pd.read_csv(call_dataset_name)
    
    global service_data

    service_data = pd.read_csv(service_dataset_name)

    global device_data

    device_data = pd.read_csv(device_dataset_name)
    temp_list = sorted(call_data['date'].dropna().unique().tolist())

    # Dropdown does not take list of string

    # It takes list of dictionary 

    global start_date_list

    start_date_list =[ { "label": str(i), "value" :str(i) }   for i in temp_list ]

    global end_date_list

    end_date_list =[ { "label": str(i), "value" :str(i) }   for i in temp_list ]

    temp_list = ['Hourly','Daywise','Weekly']

    global report_type

    report_type = [ {"label":str(i) , "value":str(i) }   for i in temp_list]
    
    print("End of the load_data function")
    
    
def open_browser():

    webbrowser.open_new('http://127.0.0.1:8050/')
    
# Layout of your page

def create_app_ui():

    # Create the UI of the Webpage here

    main_layout = html.Div([

    

    html.H1('CDR Analysis with Insights', id='Main_title'),

    

    dcc.Tabs(id="Tabs", value="tab-1",children=[

    dcc.Tab(label="Call Analytics tool" ,id="Call Analytics tool",value="tab-1", children = [

    html.Br(),

    html.Br(),

    

    dcc.Dropdown(

          id='start-date-dropdown', 

          options=start_date_list,

          placeholder = "Select Starting Date here",

          value = "2019-06-20"

    ),

            

    dcc.Dropdown(

           id='end-date-dropdown', 

                  options=end_date_list,

                  placeholder = "Select Ending Date here",

                  value = "2019-06-25"

    ),

            

            

    dcc.Dropdown(

                  id='group-dropdown', 

                  placeholder = "Select group here",

                  multi = True

    ),

            

            

    dcc.Dropdown(

                  id='Report-type-dropdown', 

                  options=report_type,

                  placeholder = "Select Report Type",

                  value = "Hourly"

    )]),

    dcc.Tab(label = "Device Analytics tool", id="Device Analytics tool", value="tab-2", children = [            

    html.Br(),

    dcc.Dropdown(

      id='device-date-dropdown', 

      options=start_date_list,

      placeholder = "Select Date here",

      multi = True

        ), 

    html.Br()]),

  

    dcc.Tab(label = "Service Analytics tool", id="Service Analytics tool", value="tab-3", children = [            

    html.Br(),

    dcc.Dropdown(

      id='service-date-dropdown', 

      options=start_date_list,

      placeholder = "Select Date here",

      multi = True

        ), 

    html.Br()])

    ]),

    html.Br(),

    dcc.Loading(html.Div(id='visualization-object',children='Graph,Card, Table')),

    

    ])

    return main_layout


def create_card(title, content, color):

    card = dbc.Card(

        dbc.CardBody(

            [

                html.H4(title, className="card-title"),

                html.Br(),

                html.Br(),

                html.H2(content, className="card-subtitle"),

                html.Br(),

                ]

        ),

        color=color, inverse=True

    )

    return(card)


def count_devices(data):

    

    # Various devices used for VoIP calls

    device_dict = {"Polycom" :0,

    "Windows" : 0,

    "iphone" : 0,

    "Android" : 0,

    "Mac" : 0,

    "Yealink" : 0,

    "Aastra" : 0,

    "Others" : 0}

    

    

    

    reformed_data = data["UserDeviceType"].dropna().reset_index()

    for var in reformed_data["UserDeviceType"]:

        if re.search("Polycom", var) :

            device_dict["Polycom"]+=1

        elif re.search("Yealink", var):

            device_dict["Yealink"]+=1

        elif re.search("Aastra", var):

            device_dict["Aastra"]+=1

        

        elif re.search("Windows", var):

            device_dict["Windows"]+=1

        elif re.search("iPhone|iOS", var):

            device_dict["iphone"]+=1

        elif re.search("Mac", var):

            device_dict["Mac"]+=1

        elif re.search("Android", var):

            device_dict["Android"]+=1

            

        else:

            device_dict["Others"]+=1

    final_data = pd.DataFrame()

    final_data["Device"] = device_dict.keys()

    final_data["Count"] = device_dict.values()

    return final_data


# Callback of your page

@app.callback(

    Output('visualization-object', 'children'),

    [

    Input("Tabs", "value"),

    Input('start-date-dropdown', 'value'),

    Input('end-date-dropdown', 'value'),

    Input("group-dropdown", 'value'),

    Input('Report-type-dropdown', 'value'),

    Input('device-date-dropdown', 'value'),

    Input('service-date-dropdown', 'value')

    

    ]

    )


def update_app_ui(Tabs, start_date, end_date, group, report_type,device_date,service_date):

    

    print("Data Type of start_date value = " , str(type(start_date)))

    print("Data of start_date value = " , str(start_date))

    

    print("Data Type of end_date value = " , str(type(end_date)))

    print("Data of end_date value = " , str(end_date))

    

    

    print("Data Type of group value = " , str(type(group)))

    print("Data of group value = " , str(group))

    

    print("Data Type of report_type value = " , str(type(report_type)))

    print("Data of report_type value = " , str(report_type))

    

    print("Data Type of device_date value = " , str(type(device_date)))

    print("Data of device_date value = " , str(device_date))


    print("Data Type of service_date value = " , str(type(service_date)))

    print("Data of service_date value = " , str(service_date))


    if Tabs == "tab-1":

        

        # Filter the data as per the selection of the drop downs

        

        call_analytics_data = call_data[ (call_data["date"]>=start_date) & (call_data["date"]<=end_date) ]

         

        if group  == [] or group is None:

           pass

        else:

           call_analytics_data = call_analytics_data[call_analytics_data["Group"].isin(group)]

         

    

    

        graph_data = call_analytics_data

        # Group the data based on the drop down     

        if report_type == "Hourly":

            graph_data = graph_data.groupby("hourly_range")["Call_Direction"].value_counts().reset_index(name = "count")

            x = "hourly_range"

            

            content = call_analytics_data["hourly_range"].value_counts().idxmax()

            title =  "Busiest Hour"

        

            

        elif report_type == "Daywise":

            graph_data = graph_data.groupby("date")["Call_Direction"].value_counts().reset_index(name = "count")

            x = "date"

            

            content = call_analytics_data["date"].value_counts().idxmax()

            title =  "Busiest Day"

            

        else:

            graph_data = graph_data.groupby("weekly_range")["Call_Direction"].value_counts().reset_index(name = "count")

            x = "weekly_range"

            

            content = call_analytics_data["weekly_range"].value_counts().idxmax()

            title =  "Busiest WeekDay"

            

           

        # Graph Section

        figure = px.area(graph_data, 

                         x = x, 

                         y = "count",

                         color = "Call_Direction",

                         hover_data=[ "Call_Direction", "count"], 

                         template = "plotly_dark")

        figure.update_traces(mode = "lines+markers")

      

      

      

        # Card Section

        total_calls = call_analytics_data["Call_Direction"].count()

        card_1 = create_card("Total Calls",total_calls, "success")

          

        incoming_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"]=="Incoming"].count()

        card_2 = create_card("Incoming Calls", incoming_calls, "primary")

          

        outgoing_calls = call_analytics_data["Call_Direction"][call_analytics_data["Call_Direction"]=="Outgoing"].count()

        card_3 = create_card("Outgoing Calls", outgoing_calls, "primary")

          

        missed_calls = call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"] == 19].count()

        card_4 = create_card("Missed Calls", missed_calls, "danger")

          

        max_duration = call_analytics_data["duration"].max()

        card_5 = create_card("Max Duration", f'{max_duration} min', "dark")

        

        card_6 = create_card(title, content, "primary")

             

      

    

        graphRow0 = dbc.Row([dbc.Col(id='card1', children=[card_1], md=3), dbc.Col(id='card2', children=[card_2], md=3)])

        graphRow1 = dbc.Row([dbc.Col(id='card3', children=[card_3], md=3), dbc.Col(id='card4', children=[card_4], md=3)])

        graphRow2 = dbc.Row([dbc.Col(id='card5', children=[card_5], md=3), dbc.Col(id='card6', children=[card_6], md=3)])

     

        cardDiv = html.Div([graphRow0,html.Br(), graphRow1,html.Br(), graphRow2])

        

    

    

    

    

        # Data Table Section

    

        datatable_data = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["Call_Direction"].value_counts().unstack(fill_value = 0).reset_index()

        if call_analytics_data["Missed Calls"][call_analytics_data["Missed Calls"]==19].count()!=0:

            datatable_data["Missed Calls"] = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["Missed Calls"].value_counts().unstack()[19]

        else:

            datatable_data["Missed Calls"] = 0

            

        datatable_data["Total_call_duration"] = call_analytics_data.groupby(["Group", "UserID", "UserDeviceType"])["duration"].sum().tolist()

        

      

    

        datatable = dt.DataTable(

        id='table',

        columns=[{"name": i, "id": i} for i in datatable_data.columns],

        data=datatable_data.to_dict('records'),

        page_current=0,

        page_size=5,

        page_action='native',

        style_header={'backgroundColor': 'rgb(30, 30, 30)'},

        style_cell={

            'backgroundColor': 'rgb(50, 50, 50)',

            'color': 'white'

        }

        )

        

            

        return [

                dcc.Graph(figure = figure), 

                html.Br() ,

                cardDiv, 

                html.Br(),

                datatable

               ]

    

    elif Tabs == "tab-2":

        if device_date is None or device_date == []: 

            device_analytics_data = count_devices(device_data)

        else:

            device_analytics_data = count_devices(device_data[device_data["DeviceEventDate"].isin(device_date)])

          

        fig = px.pie(device_analytics_data, names = "Device", values = "Count", color = "Device", hole = .3)

        fig.update_layout(autosize=True,

                          margin=dict(l=0, r=0, t=25, b=20),

                          )

        return dcc.Graph(figure = fig)

    

    

    

    

    elif Tabs == "tab-3":

        if service_date is None or service_date == []:

            service_analytics_data = service_data["FeatureName"].value_counts().reset_index(name = "Count")

        else:

            service_analytics_data = service_data["FeatureName"][service_data["FeatureEventDate"].isin(service_date)].value_counts().reset_index(name = "Count")

        fig = px.pie(service_analytics_data, names = "index", values = "Count",color = "index")

        

        fig.update_layout(autosize=True,

                          margin=dict(l=0, r=0, t=25, b=20),

                          )

        return dcc.Graph(figure = fig)

    

    else:

        return None

    

    

@app.callback(

    Output("group-dropdown", "options"),

    [

    Input('start-date-dropdown', 'value'),

    Input('end-date-dropdown', 'value')

    ]

    )

def update_groups(start_date, end_date): 

    reformed_data = call_data[(call_data["date"]>=start_date) & (call_data["date"]<=end_date)]

    group_list = reformed_data["Group"].unique().tolist()

    group_list = [{"label":m, "value":m} for m in group_list]

    return group_list


def main():  

    dataset_name = 'Forsk_Internship_Batch_6/CDR Dataset/cdr_data.csv'
    # Required columns

    call_columns = ["4", "5","14", "31", "120", "147", "267", "312", "345", \

                    "date","starttime", "endtime","duration", "hourly_range","weekly_range"]

    call_dataset = pd.read_csv(dataset_name, usecols = call_columns,low_memory = False)

    
    # coulmns for service data

    service_columns = ["31", "120", "147", "345","date", "starttime", "endtime","duration"]

    service_dataset = call_dataset[service_columns]

    # columns for device data

    device_columns = ["5", "31", "120", "312", "345", "date","starttime", "endtime","duration"]

    device_dataset = call_dataset[device_columns]

    call_dataset = call_dataset.rename(columns = {"4":"Group", "5":"Call_Direction","14":"Missed Calls",

                                            "31":"GroupID", "120":"UserID", "147":"Features", "267":" vpDialingfacResult",

                                            "312":"UsageDeviceType",

                                            "345":"UserDeviceType"})

    

    

    service_dataset = service_dataset.rename(columns={"120":"UserID", 

                                                  "31":"GroupID", "147":"FeatureName",

                                                  "345":"UserDeviceType","date":"FeatureEventDate"

                                                  })

    
    device_dataset = device_dataset.rename(columns={"5": "DeviceEventTypeDirection", 

                                      "120":"UserID", "31":"GroupID", 

                                      "345":"UserDeviceType","date":"DeviceEventDate", 

                                      "312":"UsageDeviceType"})

    call_dataset.to_csv("Call_data.csv", index=None)

    service_dataset.to_csv("Service_data.csv", index=None)

    device_dataset.to_csv("Device_data.csv", index=None)
    

    print("Start of the main function ")  

    load_data()

    open_browser()

    global project_name

    project_name = "CDR Analysis with Insights"
    
    global app

    app.layout = create_app_ui()

    app.title = project_name

    app.run_server()  # this is  an infinite loop 


    print("End of the main function ")  

    project_name = None

    app = None

    global call_data,service_data,device_data, start_date_list,end_date_list,report_type

    call_data = None

    service_data = None

    device_data = None

    start_date_list = None

    end_date_list = None

    report_type= None


if (__name__ == '__main__'):

    main()


# Creation of the cdr_data.csv file Using the filtering 
"""


cdr_dataset = pd.read_csv(dataset_name , header=None , low_memory=False)

cdr_dataset['date'], cdr_dataset['time']  = zip(*datetime_divider(cdr_dataset[9].tolist()))


print(cdr_dataset['date'] )

print(cdr_dataset['time'] )

print(cdr_dataset[9] )


print(cdr_dataset['date'] )

cdr_dataset['date'] = date_modifier( cdr_dataset['date'].tolist() )

print(cdr_dataset['date'] )


print(cdr_dataset['time'] )

cdr_dataset['time'] = time_modifier( cdr_dataset['time'].tolist() )

print(cdr_dataset['time'] )


cdr_dataset[5].unique()

cdr_dataset[267].unique()

cdr_dataset[312].unique()

cdr_dataset   =  replace_simple_with_Standard_terminology( cdr_dataset )

cdr_dataset[5].unique()

cdr_dataset[267].unique()

cdr_dataset[312].unique()

cdr_dataset[312] = remove_Unwanted_data(cdr_dataset[312].tolist())  

cdr_dataset[312].unique()
# we have made temporary 2 columns to find duration

print (cdr_dataset[9])

cdr_dataset["starttime"] = pd.to_datetime(call_time_fetcher(cdr_dataset[9].tolist()))

print(cdr_dataset["starttime"])

# 2019-06-25 19:21:43


print (cdr_dataset[13])

cdr_dataset["endtime"] = pd.to_datetime(call_time_fetcher(cdr_dataset[13].tolist()))

print(cdr_dataset["endtime"])


# 2019-06-25 19:24:54

cdr_dataset["duration"] =  (cdr_dataset["endtime"] - cdr_dataset["starttime"]).astype("timedelta64[m]")

print(cdr_dataset["duration"])

    
# use the new columns created time and date

# Creates 1 hour range for 24 hours

cdr_dataset["hourly_range"] = hourly_range(cdr_dataset["time"].tolist())

print(cdr_dataset["hourly_range"])

# 19:00 - 19:59

# Creates similary in Week ( Monday to Sunday )

cdr_dataset["weekly_range"] = weekly_range(cdr_dataset["date"].tolist())

print(cdr_dataset["weekly_range"])
# Remove columns not required

cdr_dataset = cdr_dataset.drop("time", axis=1)

# Save the transformed data in CSV format for further use

cdr_dataset.to_csv("cdr_data.csv", index = None)

"""