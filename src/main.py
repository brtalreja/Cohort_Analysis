#Importing required libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_white"

data = pd.read_csv("../data/cohorts.csv")

print(data.head())