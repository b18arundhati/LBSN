import pickle
import os
import json
import ast
import numpy as np  
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
business_id=load_pickle('./pre_data/business_id_mapping.pkl')
user_business_review=load_pickle('./pre_data/user_business_review.pkl')
category_stats={}
Bid_category_lst={}
def update_category(id_,line_dict):
    try:
        categories=line_dict['categories'].replace('&',',').split(',')
#        print(categories)
        Bid_category_lst[id_]=[]
        for category in categories:
            cate=category.lower().strip()
            Bid_category_lst[id_].append(cate)
            try:
                category_stats[cate]+=1
            except:
                category_stats[cate]=1
    except:
        Bid_category_lst[id_]=[]
#        return
    return 
def category_selection():
    id_category_top={}
    for id_ in Bid_category_lst:
        catgr_lst=Bid_category_lst[id_]
#        print(id_,catgr_lst)
        dic={}
        for cat in catgr_lst:
            dic[cat]=category_stats[cat]
        catgr_lst=sorted(dic,key=dic.get,reverse=True)
        id_category_top[id_]=catgr_lst[:5]
    return id_category_top

user_business_category={}
def user_business_preference():
    for user in user_business_review:
        business_review=user_business_review[user]
#        print(user,business_review.keys())
        category_list=np.array([])
        for business in business_review:
            category_list=np.concatenate((category_list,np.array(Bid_category_lst[business])))
#            print(Bid_category_lst[business])
        dic={}
        for cat in category_list:
            dic[cat]=category_stats[cat]
        catgr_lst=sorted(dic,key=dic.get,reverse=True)
        user_business_category[user]=catgr_lst[:5]
#        print(id_,user_business_category[user])
    print(len(user_business_category.keys()))

attribute_id={}
#attribute_status={}
attribute_status={'False': 0, 'True': 1, False: 0, True: 1, 'average': 'average', 'casual': 'casual', '2': 2, 'none': 0, 'no': 0, 'beer_and_wine': 'beer_and_wine', 'free': 1, '1': 1, 'loud': 'loud', 'full_bar': 'full_bar', 'yes_free': 1, 'outdoor': 'outdoor', 'quiet': 'quiet', 'dressy': 'dressy', '3': 3, 'very_loud':'very_loud', 'paid':0 , 'formal': 'formal', '18plus': '18plus', 'yes': 1, '4': 4, 'allages': 'allages', '19plus': '19plus', 'yes_corkage': 1, '21plus': '21plus'}

businessId_attribute_lst={}
def update_attributes(id_,line_dict):
#    print(id_,line_dict['attributes'])
    try:
        attributes=line_dict['attributes']
        if not attributes:
            x=1/0#just to raise an error
    except:
        businessId_attribute_lst[id_]=[]
        return 
    att_feat={}
#    print(attributes)
    for attribute in attributes:
        att=attribute.strip().lower()
        status=attributes[attribute]
        if(str(status)[0]=='{'):
            dic=ast.literal_eval(str(status))
            for k in dic:
                attr=str(att)+'_'+str(k)
#                attribute_status[dic[k]]=1
                if attr not in attribute_id:
                    attribute_id[attr]=len(attribute_id.keys())
                att_feat[attribute_id[attr]]=attribute_status[dic[k]]
                
        else:
            
#                attribute_status[status]=1
            if att not in attribute_id:
                attribute_id[att]=len(attribute_id.keys())
            att_feat[attribute_id[att]]=attribute_status[status]

    feat_vec=[]
    for i in range(len(attribute_id.keys())):
         if i in att_feat:
             feat_vec.append(att_feat[i])
         else:
             feat_vec.append(-1)
    businessId_attribute_lst[id_]=feat_vec
#    print(feat_vec)     
    
def business_attribute_lst():
    
    for business in businessId_attribute_lst:
        lst=businessId_attribute_lst[business]
        length=len(lst)
        for i in range(len(attribute_id.keys())-length):
            lst.append(-1)
        businessId_attribute_lst[business]=tuple(lst)
        
business_count=0
while True:
#for i in range(10):
    try:
        line=json_data.readline()
        line_dict=json.loads(line.strip())
        business_name=line_dict["business_id"]
        id_=business_id[business_name]
        update_category(id_,line_dict)
        update_attributes(id_,line_dict)
        business_count+=1
        if business_count%10000==0:
            print(business_count)
    except:
        break
user_business_preference()
id_top_category=category_selection()
save_pickle('./pre_data/businessId_categories.pkl',id_top_category)
save_pickle('./pre_data/userId_businessCategoryList.pkl',user_business_category)
business_attribute_lst()
save_pickle('./pre_data/businessId_attribute_lst.pkl',businessId_attribute_lst)
save_pickle('./pre_data/businessAttribute_index.pkl',attribute_id)
#print(attribute_id)  
#print(businessId_attribute_lst)      
#print(attribute_status)