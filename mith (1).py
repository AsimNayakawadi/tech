# -*- coding: utf-8 -*-
"""MITH.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UuWImBPSo2Ge0e2CC4nMJTfFEes6oUVj

Import Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
##for modelling
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.svm import SVC,SVR

from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm

"""Reading data"""

from google.colab import drive
drive.mount("/content/gdrive")

import os 
PATH = "/content/gdrive/MyDrive/Mith"
os.chdir(PATH)

data1 = pd.read_csv('Insurance_Claim_Info_data.csv')

data2 = pd.read_csv('Insurance_Date_data.csv')

test_data = pd.read_csv("test_data-1663477366404.csv")

"""for test data"""

test_data.head()

datax=test_data.drop(['Incident Date','Claim Number','Date Received'],axis=1)

datax.select_dtypes(include="object").columns

col1 = ['City Code', 'City', 'Enterprise Type', 'Claim Type', 'Claim Site',
       'Product Insured']

datax[col1] = datax[col1].astype('category')

"""Merging data

"""

mdata = pd.merge(data1, data2)

mdata

data3 = pd.read_csv('Insurance_Result_data.csv')

data3

Wdata = pd.merge(mdata, data3)

Wdata

"""Exploratory Data Anlysis"""

Wdata.shape

Wdata.head()

Wdata.tail()

Wdata.columns

Wdata.describe()

Wdata.info()

Wdata.isna().sum()

"""Describing target """

Wdata['Disposition'].describe()

Wdata['Disposition'].value_counts()

Wdata.dtypes

Wdata.nunique()

"""Took an extra column for Reporting delay

"""

Wdata[['Date Received','Incident Date']] = Wdata[['Date Received','Incident Date']].apply(pd.to_datetime) #if conversion required
Wdata['Reporting delay'] = (Wdata['Date Received'] - Wdata['Incident Date']).dt.days

Wdata.dtypes

Wdata.head()

Wdata.tail()

Wdata['% of claim'] = (Wdata['Claim Amount'] / 
                      Wdata['Claim Amount'].sum()) * 100

Wdata.dtypes

"""## changing the object into category"""

Wdata['Disposition'] = data4['Disposition' ].astype('category')

np.isnan(Wdata.any()) #and gets False
np.isfinite(Wdata.all()) #and gets True

Wdata.head()

"""Data Visualisation"""

sns.heatmap(Wdata.corr())

sns.distplot(Wdata['Claim Amount'])

sns.histplot(Wdata,x='Claim Site')





"""Data Visualisation ends"""

data4=Wdata.drop(['Incident Date','Date Received','Reporting delay','% of claim','Claim Number'],axis=1)

x= data4.drop(["Disposition"],axis=1)
y=data4['Disposition']

"""Train and Test Split"""

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=101)

x_train

data4.dtypes

data4.select_dtypes(include="object").columns

col = [ 'City Code', 'City', 'Enterprise Type', 'Claim Type',
       'Claim Site', 'Product Insured']

data4[col] = data4[col].astype('category')

data4.dtypes

data4.info()

data4.head()

data4.select_dtypes(include="float64").columns

num = ['Claim Amount', 'Close Amount']

data4.isnull().sum()

"""Imputation"""

col_imputer = SimpleImputer(strategy='most_frequent')
num_imputer = SimpleImputer(strategy='mean')

x_train_num=x_train.drop(col,axis=1)
x_train_col=x_train.drop(num,axis=1)

x_test_num=x_test.drop(col,axis=1)
x_test_col=x_test.drop(num,axis=1)
x_train.columns

x_train_num=pd.DataFrame(num_imputer.fit_transform(x_train_num),columns=x_train_num.columns)
x_train_col=pd.DataFrame(col_imputer.fit_transform(x_train_col),columns=x_train_col.columns)

x_test_num=pd.DataFrame(num_imputer.transform(x_test_num),columns=x_test_num.columns)
x_test_col=pd.DataFrame(col_imputer.transform(x_test_col),columns=x_test_col.columns)

x_test_col.isna().sum()

"""Standardization of the Data"""

# standardization of numeric data
scaler = StandardScaler()

x_train_num=pd.DataFrame(scaler.fit_transform(x_train_num),columns=x_train_num.columns)
x_test_num=pd.DataFrame(scaler.transform(x_test_num),columns=x_test_num.columns)

x_train_num.shape

data4.nunique()

#one hot encoding

"""One Hot Encoding"""

ohe = OneHotEncoder(handle_unknown='ignore')

x_train_col = pd.DataFrame(ohe.fit_transform(x_train_col).todense(), columns = ohe.get_feature_names_out())

x_train_col.head()

x_test_col = pd.DataFrame(ohe.transform(x_test_col).todense(), columns = ohe.get_feature_names_out())

x_test_col.head()



## Combining Numeric and Categorical Data - use concat

Train = pd.concat([x_train_num,x_train_col],axis=1)

Test = pd.concat([x_test_num, x_test_col],axis=1)

Test.head()

Test2 = datax

Train.shape

Train.head()

"""Model Building

Logistic regression
"""

from sklearn.linear_model import LogisticRegression

y_train = y_train.astype('category')
y_test = y_test.astype('category')

model = LogisticRegression(solver = 'liblinear', random_state=0)

model.fit(Train, y_train)

log_pred=model.predict(Train)

logT_pred=model.predict(Test)



confusion_matrix(y_train,log_pred)

confusion_matrix(y_test,logT_pred)

print(classification_report(y_train,log_pred))

print(classification_report(y_test,logT_pred))

"""Support Vector Machine"""

mod=SVC(kernel='rbf',C=2)
mod.fit(Train,y_train)

preds_train=mod.predict(Train)

preds_test=mod.predict(Test)

confusion_matrix(y_train,preds_train)

confusion_matrix(y_test,preds_test)

print(classification_report(y_test,preds_test))

