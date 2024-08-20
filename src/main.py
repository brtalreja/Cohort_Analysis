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
# The number of new users show a repetitive pattern with peaks and troughs. This can be due to implementing marketing campaigns, any seasonal trends, or other factors which drive new user acquisition.
# There is a need to understand why there was a spike in the number of new users and how to sustain that growth.
# Most of the times the returning number of users were less fluctuating. This can be good and bad.
# Good because the numbers are consistent which means a good retention rate.
# Bad because there is no increase in retention rate.
# A significant difference is there in the number of new users and returning users which indicates high churn rate.

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
# The duration on Day 1 shows less fluctuations compared to day 7. There is a big spike around mid-November which means that duration significantly increased at that time.
# There is a noticeable downward trend towards the end of the period meaning that initial user engagement is decreasing over time. This could be due to a variety of factors, such as changes in the user experience, content, or platform performance.
# The duration on Day 7 shows more variability and a slight decreasing trend overall. There are periods where the Day 7 duration drops to zero, indicating that users are not returning or spending time on the platform a week after their initial use.
# The sharp drop to zero towards the end of the period is particularly concerning, as it suggests a failure to retain users beyond the first day during this time frame.
# The Day 7 duration is consistently lower than the Day 1 duration, indicating a decline in user engagement over time. This suggests that users may find less value or are less interested in returning to the platform after their initial experience.
# The wide gap between Day 1 and Day 7 durations in certain periods indicates that the initial interest is not translating into long-term engagement.

# Retention strategies such as follow-up emails, push notifications, or personalized content should be implemented to encourage users to return to the platform.
# The initial experience (Day 1) is crucial in setting the tone for continued engagement. Enhancing the onboarding process, providing clear guidance on how to use the platform, and highlighting key features could help boost the retention rate.
# Perform a detailed analysis of the content and user journey to identify any pain points where users might be dropping off to understand user's perspective.

#Correlation Analysis
correlation_matrix = data.corr()

plt.figure(figsize=(10,8))
sns.heatmap(correlation_matrix, annot = True, cmap = "coolwarm", fmt = ".2f")
plt.title('Correlation Plot of Metrics')

plt.savefig("../output/Correlation_Plot.png")

plt.show()

#COMMENT: 
# There is a strong positive correlation between new users and returning users suggesting that on days when more new users join, more existing users also return to the platform.
# There is a strong negative correlation between the date and Duration Day 7 which implies that over time, the duration that users spend on the platform on the 7th day after their first interaction decreases significantly.
# This is a concerning trend as it indicates a decline in user satisfaction over time.

# The strong positive correlation between new and returning users presents an opportunity to capitalize on days with high traffic.
# It may be useful to analyze user feedback or behavior patterns to identify any issues leading to this trend.
# Another possible strategies to look into are: continuous monitoring of returning user trends and optimizing day 1 experience for new users.

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

#COMMENT:
# There is a noticeable increase in the number of new users then a slight decline and finishing with a steep incline.
# The number of returning users remains relatively stable across the weeks with minor fluctuations.
# A small upward trend is observed in Week 47, but the increase is modest compared to the increase in the number of new users.
# New users consistently outnumber returning users across all weeks.

figure2.show()
figure2.write_image("../output/Weekly_Average_Duration.png")

#COMMENT:
# The average duration on Day 1 remains relatively stable between weeks 43 and 45 with a slight increase in week 46. However, there is a noticeable drop in week 47. This suggests that new users are generally engaged on the platform.
# The average duration on Day 7 shows a consistent decline from week 43 to week 47. By week 47, the average duration on Day 7 drops to almost zero, indicating a significant drop-off in user engagement after the first week of use.
# While the duration on Day 1 remains relatively stable, the sharp decline in Day 7 duration highlights a growing divergence between the initial and long-term engagement.


#Cohort Matrix

cohort_matrix = weekly_averages.set_index('Week')

plt.figure(figsize=(12,8))

sns.heatmap(cohort_matrix, annot = True, cmap = "coolwarm", fmt = ".1f")
plt.title('Cohort Matrix of Weekly Averages')
plt.ylabel('Week of the Year')

plt.savefig("../output/Cohort_Matrix_plot.png")

plt.show()

#COMMENT:

#Retention Rate Analysis

data['Retention Rate'] = (data['Returning users'] / data['New users']) * 100
print(data[['Date', 'Retention Rate']].head())

#COMMENT:

#Chrun Rate Analysis

data['Churn Rate'] = 100 - data['Retention Rate']
print(data[['Date', 'Churn Rate']].head())

#COMMENT:

#User growth rate analysis

data['New User Growth Rate'] = data['New users'].pct_change() * 100
print(data[['Date', 'New User Growth Rate']].head())

#COMMENT:

#Daily Engagement Analysis

figure = px.scatter(data, x='New users', y=['Duration Day 1', 'Duration Day 7'], trendline='ols',
                    title='New Users vs. Duration on Day 1 and Day 7')
figure.show()

figure.write_image('../output/New_Users_Day1_Day7.png')

figure = px.scatter(data, x='Returning users', y=['Duration Day 1', 'Duration Day 7'], trendline='ols',
                    title='Returning Users vs. Duration on Day 1 and Day 7')
figure.show()

figure.write_image('../output/Returning_Users_Day1_Day7.png')

#COMMENT:

#Rolling Averages

data['Rolling Avg New Users'] = data['New users'].rolling(window=7).mean()
data['Rolling Avg Returning Users'] = data['Returning users'].rolling(window=7).mean()

figure = go.Figure()
figure.add_trace(go.Scatter(x=data['Date'], y=data['Rolling Avg New Users'], mode='lines+markers', name='Rolling Avg New Users'))
figure.add_trace(go.Scatter(x=data['Date'], y=data['Rolling Avg Returning Users'], mode='lines+markers', name='Rolling Avg Returning Users'))

figure.update_layout(title='Rolling Average of Users',
                     xaxis_title='Date',
                     yaxis_title='Number of Users')
figure.show()

figure.write_image('../output/Rolling_Averages_Day1_Day7.png')

#COMMENT: