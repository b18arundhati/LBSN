#import nltk
#import numpy as np
#from nltk.tokenize import RegexpTokenizer
#import string
#from collections import OrderedDict
import pickle
#import math
import os
import json
#from scipy import stats
#import matplotlib.pyplot as plt
from constants import *

def load_pickle(filename):
    file=open(filename,'rb')
    object_file=pickle.load(file)
    return object_file

def save_pickle(filename,fileobject):
    filehandler=open(filename,"wb")
    pickle.dump(fileobject,filehandler)
    filehandler.close()
    
    

json_data=open(os.path.join(data_folder,business_json))
business_id={}
id_business={}
businessId_lat_long={}
#user_friends={}
business_count=0
while True:
    try:
        line=json_data.readline()
        line_dict=json.loads(line.strip())
#        print(line_dict)
        business_name=line_dict["business_id"]
        latitude=line_dict["latitude"]
        longitude=line_dict["longitude"]
        business_id[business_name]=business_count
        id_business[business_count]=business_name
        businessId_lat_long[business_count]=(latitude,longitude)
        business_count+=1
        if business_count%100000==0:
            print(business_count)
#        user_friends[user_name]=line_dict["friends"]
#        break
    except:
        break
print(business_count)
print(len(business_id.keys()))
save_pickle('./pre_data/id_business_mapping.pkl',id_business)
save_pickle('./pre_data/business_id_mapping.pkl',business_id)
save_pickle('./pre_data/businessId_lat_long.pkl',businessId_lat_long)
print(len(id_business.keys()))
print(len(business_id.keys()))
print(len(businessId_lat_long.keys()))

#save_pickle('./pre_data/friend_list.pkl',user_friends_id)






    