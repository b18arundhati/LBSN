import pickle
import os
import json
import ast
import numpy as np  
import collections
from constants import *
def load_pickle(filename):
    file=open(filename,'rb')
    object_file=pickle.load(file)
    return object_file
def save_pickle(filename,fileobject):
    filehandler=open(filename,"wb")
    pickle.dump(fileobject,filehandler)
    filehandler.close()

user_friends=load_pickle('./pre_data/friend_list.pkl')
user_loc=load_pickle('./pre_data/userId_lat_long.pkl')
user_bus_cat=load_pickle('./pre_data/userId_businessCategoryList.pkl')
user_bias=load_pickle('./pre_data/userId_bias.pkl')
print(len(user_loc))

for user in user_friends:
#    x=user_bias[user]
    if len(user_friends[user])>50:
        user_=user
        break
def get_distance(a,b):
    loc_a=user_loc[a]
    loc_b=user_loc[b]
    print(loc_a,loc_b)
    dist=0
    
    return dist
    
def get_cat_overlap(a,b):
    cat_a=user_bus_cat[a]
    cat_b=user_bus_cat[b]
    score=len(list(set(cat_a).intersection(set(cat_b))))
    score=float(score)/(min(len(cat_a),len(cat_b)))
    return score

friend_lst=user_friends[user_]
for friend in friend_lst:
    if friend<0:
        continue
    overlap_coeff=get_cat_overlap(user_,friend)
    try:
        dist=get_distance(user_,friend)
    except:
        continue
#    try:
    sentiment=np.abs(user_bias[user_]-user_bias[friend])
#    except:
#        sentiment=-1

