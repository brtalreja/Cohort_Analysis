#Importing required libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_white"

data = pd.read_csv("../data/cohorts.csv")

print(data.head())

#Check if the data has missing values:
missing_values = data.isnull().sum()
print(missing_values)

# COMMENT: No columns have missing values.

#Check the datatypes of all the columns:
data_types = data.dtypes
print(data_types)

# COMMENT: We can observe that the date column is in the Object (string) format. In our analysis, we will need this to be in a datetime format.

#Converting the datatype of date column.
data['Date'] = pd.to_datetime(data['Date'], format = '%d/%m/%Y')

#Rechecking the data types to confirm the change.
data_types = data.dtypes
print(data_types)

#Descriptive stats about the data.
stats = data.loc[:, data.columns != "Date"].describe()
print(stats)

# COMMENT: 