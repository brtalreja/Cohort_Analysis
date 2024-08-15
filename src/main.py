#Importing required libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
import seaborn as sns

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
# All the metrics show significant variability. While the average numbers are high, there is a broad range which indicates diversity in user engagement and variation in user engagement from day to day.

#EDA

#Trend analysis
figure = go.Figure()

figure.add_trace(go.Scatter(
                x = data['Date'],
                y = data['New users'],
                mode = 'lines+markers',
                name = 'New users'))

figure.add_trace(go.Scatter(
                x = data['Date'],
                y = data['Returning users'],
                mode = 'lines+markers',
                name = 'Returning users'))

figure.update_layout(title = 'Trend of New Users and Returning Users Over Time',
                     xaxis_title = 'Date',
                     yaxis_title = 'Number of Users')

figure.show()

figure.write_image("../output/Trend_Plot_New_users_Returning_users.png")

#Trend of duration over time
figure = go.Figure()

figure.add_trace(go.Scatter(
                x = data['Date'],
                y = data['Duration Day 1'],
                mode = 'lines+markers',
                name = 'Duration Day 1'))

figure.add_trace(go.Scatter(
                x = data['Date'],
                y = data['Duration Day 7'],
                mode = 'lines+markers',
                name = 'Duration Day 7'))

figure.update_layout(title = 'Trend of Duration Over Time',
                     xaxis_title = 'Date',
                     yaxis_title = 'Duration')

figure.show()

figure.write_image("../output/Trend_Plot_Duration.png")

#Correlation Analysis
correlation_matrix = data.corr()

plt.figure(figsize=(10,8))
sns.heatmap(correlation_matrix, annot = True, cmap = "coolwarm", fmt = ".2f")
plt.title('Correlation Plot of Metrics')
plt.show()

plt.savefig("../output/Correlation_Plot.png")