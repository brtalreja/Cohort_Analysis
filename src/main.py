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

#COMMENT:

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

#COMMENT:

#Correlation Analysis
correlation_matrix = data.corr()

plt.figure(figsize=(10,8))
sns.heatmap(correlation_matrix, annot = True, cmap = "coolwarm", fmt = ".2f")
plt.title('Correlation Plot of Metrics')

plt.savefig("../output/Correlation_Plot.png")

plt.show()

#COMMENT:

#Cohort Analysis

data['Week'] = data['Date'].dt.isocalendar().week

weekly_averages = data.groupby('Week').agg({
    'New users': 'mean',
    'Returning users': 'mean',
    'Duration Day 1': 'mean',
    'Duration Day 7': 'mean'
}).reset_index()

print(weekly_averages.head())

figure1 = px.line(weekly_averages,
                  x = 'Week',
                  y = ['New users', 'Returning users'],
                  markers=True,
                  labels = {'value': 'Average Number of Users'},
                  title = 'Weekly Average of New vs. Returning Users')

figure1.update_xaxes(title = 'Week of the Year')
figure1.update_yaxes(title = 'Average Number of Users')

figure2 = px.line(weekly_averages,
                  x = 'Week',
                  y = ['Duration Day 1', 'Duration Day 7'],
                  markers=True,
                  labels = {'value': 'Average Duration'},
                  title = 'Weekly Average of Duration (Day1 vs. Day 7)')

figure2.update_xaxes(title = 'Week of the Year')
figure2.update_yaxes(title = 'Averahe Duration')

figure1.show()
figure1.write_image("../output/Weekly_Average_Users.png")

figure2.show()
figure2.write_image("../output/Weekly_Average_Duration.png")

#COMMENT:

#Cohort Matrix

cohort_matrix = weekly_averages.set_index('Week')

plt.figure(figsize=(12,8))

sns.heatmap(cohort_matrix, annot = True, cmap = "coolwarm", fmt = ".1f")
plt.title('Cohort Matrix of Weekly Averages')
plt.ylabel('Week of the Year')

plt.savefig("../output/Cohort_Matrix_plot.png")

plt.show()

#COMMENT: