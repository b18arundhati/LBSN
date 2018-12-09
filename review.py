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

json_data=open(os.path.join(data_folder,review_json))
business_id=load_pickle('./pre_data/business_id_mapping.pkl')
user_id=load_pickle('./pre_data/user_id_mapping.pkl')
id_text={}
review_id={}
id_review={}
review_count=0
business_user_review={}
user_business_review={}
review_actual=0
num_review_used=0
while True:
#for i in range(10):
    try:
        line=json_data.readline()
        line_dict=json.loads(line.strip())
#        print(line_dict)
        review_name=line_dict["review_id"]
        review_id[review_name]=review_count
        id_review[review_count]=review_name
        id_text[review_count]=line_dict["text"]
        review_count+=1
        if review_count%100000==0:
            print(review_count)
        try:
            userId=user_id[line_dict["user_id"]]
            businessId=business_id[line_dict["business_id"]]
            if userId in user_business_review:
                dic=user_business_review[userId]
                if businessId in dic:
                    lst=dic[businessId]
                    lst.append(review_count-1)
                else:
                    lst=[(review_count-1)]
                dic[businessId]=lst
                user_business_review[userId]=dic
            else:
                user_business_review[userId]={}
                user_business_review[userId][businessId]=[review_count-1]
#           
                
            if businessId in business_user_review:
                dic=business_user_review[businessId]
                if userId in dic:
                    lst=dic[userId]
                    lst.append(review_count-1)
                else:
                    lst=[(review_count-1)]
                dic[userId]=lst
                business_user_review[businessId]=dic
            else:
                business_user_review[businessId]={}
                business_user_review[businessId][userId]=[review_count-1]
#            print(business_user_review[businessId])
#            print(line_dict)
            review_actual+=1
#            print(businessId)
        except:
            continue
    except:
        break
print('total_reviews = '+str(review_count))
print('reviews which we will use = '+str(review_actual))
print('We have data for '+str(len(business_user_review.keys()))+' businesses')
save_pickle('./pre_data/id_business_mapping.pkl',id_review)
save_pickle('./pre_data/business_id_mapping.pkl',review_id)
save_pickle('./pre_data/business_user_review.pkl',business_user_review)
save_pickle('./pre_data/user_business_review.pkl',user_business_review)
save_pickle('./pre_data/reviewId_text.pkl',id_text)
#total_reviews = 5996996
#reviews which we will use = 5996996
#We have data for 188593 businesses