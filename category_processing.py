import pickle
import os
import json
import ast
import numpy as np  
import matplotlib.pyplot as plt
from constants import *
from collections import defaultdict
def load_pickle(filename):
    file=open(filename,'rb')
    object_file=pickle.load(file)
    return object_file
def save_pickle(filename,fileobject):
    filehandler=open(filename,"wb")
    pickle.dump(fileobject,filehandler)
    filehandler.close()
    
json_data=open(os.path.join(data_folder,business_json))
business_user_review=load_pickle('./pre_data/business_user_review.pkl')
business_id=load_pickle('./pre_data/business_id_mapping.pkl')
user_business_review=load_pickle('./pre_data/user_business_review.pkl')
category_stats={}
Bid_category_lst={}
user_business_category={}

def update_BId_category(id_,line_dict):
    try:
        categories=line_dict['categories'].replace('&',',').split(',')
#        print(categories)
        Bid_category_lst[id_]=[]
        for category in categories:
            cate=category.lower().strip()
            Bid_category_lst[id_].append(cate)
    except:
        Bid_category_lst[id_]=[]
#        return
    return 
def make_plot_data(stats,filename,x_axis,y_axis):
    cat_Lst=sorted(stats,key=stats.get,reverse=True)
    freq=[]
    cat_lst=cat_Lst[:10]
    max_freq=float(stats[cat_lst[0]])
    for cat in cat_lst:
        freq.append(stats[cat]/max_freq)
    print(cat_lst)
    print(freq)
    index = np.arange(len(cat_lst))
    plt.bar(index, freq)
    plt.xlabel(x_axis, fontsize=10)
    plt.ylabel(y_axis, fontsize=10)
    plt.xticks(index, cat_lst, fontsize=8, rotation=90)
    plt.tight_layout()
    plt.savefig('./pre_data/'+filename+'.png')
    f=open('./pre_data/'+filename+'.txt','w')
    for cat in cat_Lst:
        f.write(str(cat)+' '+str(stats[cat])+'\n')
    f.close()
    plt.clf()
def compute_stats():
    ct=0
#    category_stats['total_data']=0
    for busiId in business_user_review:
        users=business_user_review[busiId]
        weightage=len(users.keys())
#        category_stats['total_data']+=weightage
#        print(busiId,weightage)
        cat_lst=Bid_category_lst[busiId]
        for cat in cat_lst:
            try:
                val=category_stats[cat]
            except:
                val=0
            category_stats[cat]=val+weightage
        ct+=1
        if (ct%10000)==0:
            print(ct)
    
    make_plot_data(category_stats,'Category_frequency','Categories','Frequency')    
        
#        if ct>10:
#            break

def business_category_selection():
    business_preferences={}
    business_preferences=defaultdict(lambda:0,business_preferences)
    id_category_top={}
    ct=0
    for id_ in Bid_category_lst:
        business_preferences['total_data']+=1
        catgr_lst=Bid_category_lst[id_]
#        print(id_,catgr_lst)
        dic={}
        for cat in catgr_lst:
            dic[cat]=category_stats[cat]
        catgr_lst=sorted(dic,key=dic.get,reverse=True)
        val=[]
        if len(catgr_lst)<3:
            index = len(catgr_lst)
        else:
            max_var=0
            index=-1
            for cat in catgr_lst:
                val.append(dic[cat])
                var=np.var(val)
                if max_var<var:
                    max_var=var
                    index=len(val)-1
        if id_<20:
            print(id_,dic,index,catgr_lst)
        id_category_top[id_]=catgr_lst[:index]
        
        business_preferences[tuple(catgr_lst[:index])]+=1
        ct+=1
        if(ct%10000==0):
            print(ct)
#        id_category_top[id_]=catgr_lst[:5]
    make_plot_data(business_preferences,'category_lst_business_frequency','category_combination','frequency')
    return id_category_top

def user_business_preference():
    user_preferences={}
    user_preferences=defaultdict(lambda:0,user_preferences)
    ct=0
    for user in user_business_review:
        user_preferences['total_data']+=1
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
        val=[]
        if len(catgr_lst)<3:
            index = len(catgr_lst)
        else:
            max_var=0
            index=-1
            for cat in catgr_lst:
                val.append(dic[cat])
                var=np.var(val)
                if max_var<var:
                    max_var=var
                    index=len(val)-1
        user_business_category[user]=catgr_lst[:index]
        user_preferences[tuple(catgr_lst[:index])]+=1
        ct+=1
        if(ct%10000==0):
            print(ct)
#        if user<5:
#            print(user)
#            print(category_list)
#            print(dic)
#            print(catgr_lst)
#            print(index)
#        user_business_category[user]=catgr_lst[:5]
#        print(id_,user_business_category[user])
    print(len(user_business_category.keys()))
    make_plot_data(user_preferences,'category_lst_user_frequency','category_combination','frequency')
    
business_count=0
while True:
    try:
        line=json_data.readline()
        line_dict=json.loads(line.strip())
#        print(line_dict['categories'])
#        print()
        business_name=line_dict["business_id"]
        id_=business_id[business_name]
        update_BId_category(id_,line_dict)
        business_count+=1
        if business_count%10000==0:
            print(business_count)
#        if business_count>10:
#            break
    except:
        break
print(len(Bid_category_lst.keys()))

compute_stats()
#user_business_preference()
#Bid_top_category=business_category_selection()
#print(len(Bid_top_category.keys()))
#print(len(user_business_category.keys()))
#save_pickle('./pre_data/businessId_categories.pkl',Bid_top_category)
#save_pickle('./pre_data/userId_businessCategoryList.pkl',user_business_category)