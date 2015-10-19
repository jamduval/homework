import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics

%matplotlib inline
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/bikeshare.csv'
bikes_alt = pd.read_csv(url)#, index_col='datetime'), parse_dates=True)
bikes = pd.read_csv(url, index_col='datetime', parse_dates=True)

#dtcol2=[row[0:10] for row in bikes.datetime]
#
#bikes2 = bikes_alt
#
#bikes2['date2']=dtcol2
#
#bikes2.drop('datetime',axis=1,inplace=True)
#
#bikes3 = bikes.groupby('date2')['temp','humidity'].mean()
#bikes4 = bikes.groupby('date2')['count'].sum()
#
#bikes3['total_riders'] = bikes4.values
#
#bikes3.plot(kind='scatter',x='temp',y='total_riders')
#
#feature_cols = ['temp','humidity']
#X=bikes3[feature_cols]
#y=bikes3.total_riders
#
#linreg=LinearRegression()
#linreg.fit(X,y)
#
#print(linreg.intercept_)
#print(linreg.coef_)

bikes_res_means = bikes[['temp','humidity']].resample('D', how='mean')
bikes_res_sums = bikes[['count']].resample('D',how='sum')

bikes_needed = pd.merge(bikes_res_means,bikes_res_sums,left_index=True,right_index=True)

bikes_needed2=bikes_needed.dropna()

feature_cols2 = ['temp','humidity']
X1=bikes_needed2[feature_cols2]
y1=bikes_needed2['count']

linreg2=LinearRegression()
fit_vals = linreg2.fit(X1,y1)

print(linreg2.intercept_)
print(linreg2.coef_)

true = y1

print('MAE:', metrics.mean_absolute_error(true, pred))
print('MSE:', metrics.mean_squared_error(true, pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(true, pred)))

