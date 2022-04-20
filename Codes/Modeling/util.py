from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error 
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings 
import tensorflow as tf
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
from xgboost import XGBRegressor


import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

import sklearn.linear_model as lm
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
import sklearn.impute as im
from sklearn.preprocessing import PolynomialFeatures

from datetime import timedelta
from datetime import datetime
from tqdm import tqdm

def timekey(horizon=1, nhist=1,thin=False,total_days=286,test=False):
  if test==False:
    dkey=np.array(range(total_days))
    if thin==True: return [(dkey[i:i+nhist],[dkey[i+nhist:i+nhist+horizon][-1]]) for i in range(total_days-horizon-nhist+1)]
    if thin==False: return [(dkey[i:i+nhist],dkey[i+nhist:i+nhist+horizon]) for i in range(total_days-horizon-nhist+1)]
  
  if test==True:
    dkey=np.arange(total_days,366)
    if thin==True: return [(dkey[i:i+nhist],[dkey[i+nhist:i+nhist+horizon][-1]]) for i in range(len(dkey)-horizon-nhist+1)]
    if thin==False: return [(dkey[i:i+nhist],dkey[i+nhist:i+nhist+horizon]) for i in range(len(dkey)-horizon-nhist+1)]

def trte_split(horizon=1,nhist=1,thin=False,trkey=1,tekey=1,dfs=None,feature_name=None):
  #train
  tkey=timekey(horizon=horizon, nhist=nhist,thin=thin,total_days=286,test=False)
  label_key=np.array(tkey)[:,1]
  feature_key=np.array(tkey)[:,0]

  shape_=len(feature_name)*nhist

  x_tr=np.zeros(shape_)
  if thin==False: y_tr=np.zeros(horizon)
  else: y_tr=np.zeros(1)

  for i in tqdm(trkey):
    cache=dfs[dfs['FIPS_STR']==i]
    if cache.shape[0]==0: 
      print('passed county:', i)
      pass
    else:
      for j in np.arange(1,len(label_key)):
        feature=cache[cache['dT'].isin(feature_key[j])][feature_name].to_numpy().flatten().tolist()
        label=cache[cache['dT'].isin(label_key[j])]['Y'].tolist()
        
        x_tr=np.vstack([x_tr,feature])
        y_tr=np.vstack([y_tr,label])

  #test
  tkey=timekey(horizon=horizon, nhist=nhist,thin=thin,total_days=286,test=True)
  label_key=np.array(tkey)[:,1]
  feature_key=np.array(tkey)[:,0]

  x_te=np.zeros(shape_)
  if thin==False: y_te=np.zeros(horizon)
  else: y_te=np.zeros(1)

  for i in tqdm(tekey):
    cache=dfs[dfs['FIPS_STR']==i]
    if cache.shape[0]==0:
      print('passed county:', i)
      pass
    else:
      for j in np.arange(1,len(label_key)):
        feature=cache[cache['dT'].isin(feature_key[j])][feature_name].to_numpy().flatten().tolist()
        label=cache[cache['dT'].isin(label_key[j])]['Y'].tolist()
        x_te=np.vstack([x_te,feature])
        y_te=np.vstack([y_te,label])

  return x_tr[1:],y_tr[1:],x_te[1:],y_te[1:]

def dnnmodel(dim=1,out_dim=4):
  NN_model = Sequential()

  #input layer
  NN_model.add(Dense(128, kernel_initializer='normal',input_dim = dim, activation='relu'))

  #hidden layers
  NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
  NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
  NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
  NN_model.add(Dense(128, kernel_initializer='normal',activation='relu'))
  NN_model.add(Dense(64, kernel_initializer='normal',activation='relu'))
  NN_model.add(Dense(64, kernel_initializer='normal',activation='relu'))
  NN_model.add(Dense(32, kernel_initializer='normal',activation='relu'))

  #output layer
  NN_model.add(Dense(out_dim))

  NN_model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), 
                   optimizer='adam', metrics=tf.metrics.BinaryAccuracy(threshold=0.2))
  return NN_model