import matplotlib.pyplot as plt
import pandas as pd

%matplotlib inline

df = pd.read_csv('HR_comma_sep.csv')
plt.plot(df['column1'], df['column2'])
