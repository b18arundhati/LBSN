import pickle
import os
import json
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
user_business_tip={}
business_user_tip={}
tip_actual=0
while True:
#for i in range(10):
    try:
        line=json_data.readline()
        line_dict=json.loads(line.strip())
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
            if userId in user_business_tip:
                dic=user_business_tip[userId]
                if businessId in dic:
                    lst=dic[businessId]
                    lst.append(tip_count-1)
                else:
                    lst=[(tip_count-1)]
                dic[businessId]=lst
                user_business_tip[userId]=dic
            else:
                business_user_tip[businessId]={}
                business_user_tip[businessId][userId]=[tip_count-1]
                user_business_tip[userId]={}
                user_business_tip[userId][businessId]=[tip_count-1]
#            print(business_user_review[businessId])
#            print(line_dict)
            tip_actual+=1
#            print(businessId)
        except:
            continue
    except:
        break
print('total_tips = '+str(tip_count))
print('tips which we will use = '+str(tip_actual))
print('We have data for '+str(len(business_user_tip.keys()))+' businesses')
save_pickle('./pre_data/business_user_tipID.pkl',business_user_tip)
save_pickle('./pre_data/tipId_text.pkl',id_text)
#total_tips = 1185348
#tips which we will use = 32047
#We have data for 3496 businesses