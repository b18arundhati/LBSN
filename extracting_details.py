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
    
    

json_data=open(os.path.join(data_folder,tip_json))
business_id=load_pickle('./pre_data/business_id_mapping.pkl')
user_id=load_pickle('./pre_data/user_id_mapping.pkl')
id_text={}
tip_id={}
id_tip={}
#user_friends={}
tip_count=0
business_user_tip={}
tip_actual=0
while True:
#for i in range(10):
    try:
        line=json_data.readline()
        line_dict=json.loads(line.strip())
#        print(line_dict)
#        tip_name=line_dict["review_id"]
#        tip_id[review_name]=tip_count
#        id_tip[tip_count]=review_name
        id_text[tip_count]=line_dict["text"]
        tip_count+=1
        if tip_count%100000==0:
            print(tip_count)
        try:
            userId=user_id[line_dict["user_id"]]
            businessId=business_id[line_dict["business_id"]]
            if businessId in business_user_tip:
                dic=business_user_tip[businessId]
                if userId in dic:
                    lst=dic[userId]
                    lst.append(tip_count-1)
                else:
                    lst=[(tip_count-1)]
                dic[userId]=lst
                business_user_tip[businessId]=dic
            else:
                business_user_tip[businessId]={}
                business_user_tip[businessId][userId]=[tip_count-1]
#            print(business_user_review[businessId])
#            print(line_dict)
            tip_actual+=1
#            print(businessId)
        except:
            continue
#        user_friends[user_name]=line_dict["friends"]
#        break
    except:
        break
print('total_tips = '+str(tip_count))
#print(len(review_id.keys()))
#print(id_text)
print('tips which we will use = '+str(tip_actual))
print('We have data for '+str(len(business_user_tip.keys()))+' businesses')
#print(business_user_tip.keys())
#user_friends_id={}   
#friend_new=[]   
#for user in user_friends:
#    if user_friends[user]=='None':
#        user_friends_id[user_id[user]]=[]
##        continue
#    else:
#        friends=user_friends[user].split(',')
#        friend_lst=[]
#        flag=1
#        for friend in friends:
#            try:
#                friend_id=user_id[friend.strip()]
#                friend_lst.append(friend_id)
#            except:
#                friend_new.append(friend)
#                continue
#        user_friends_id[user_id[user]]=friend_lst
##        print(user_friends[user])
##        print(type(user_friends[user]))
##        print(user_friends[user].split(','))
#print(len(set(friend_new)))      
#save_pickle('./pre_data/id_tip_mapping.pkl',id_review)
#save_pickle('./pre_data/tip_id_mapping.pkl',tip_id)
save_pickle('./pre_data/business_user_tipID.pkl',business_user_tip)
save_pickle('./pre_data/tipId_text.pkl',id_text)
