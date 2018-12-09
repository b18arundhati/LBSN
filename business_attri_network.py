import pickle
import os
import json
import ast
import numpy as np  
import collections
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
    
bId_attri=load_pickle('./pre_data/businessId_attribute_lst.pkl')
attri_idx=load_pickle('./pre_data/businessAttribute_index.pkl')
business_user_review=load_pickle('./pre_data/business_user_review.pkl')
user_business_review=load_pickle('./pre_data/user_business_review.pkl')
def get_attribute_popularity():
    bId_attriIdx={}
    ct=0
    print('#business = ',len(bId_attri.keys()))
    for bId in bId_attri:
        attri_status=bId_attri[bId]
#        print(attri_status)
        true_attri=[]
        for i in range(len(attri_status)):
            if attri_status[i]>0:
                true_attri.append(i)
#        print(true_attri)
        bId_attriIdx[bId]=true_attri
        ct+=1
        if (ct%10000)==0:
            print(ct)
    save_pickle('./pre_data/businessId_true_Attribute_lst.pkl',bId_attriIdx)
    ct=0 
    attriId_stats={}
    attriId_stats=defaultdict(lambda:0,attriId_stats)
    for busiId in business_user_review:
        users=business_user_review[busiId]
        weightage=len(users.keys())
#        print(busiId,weightage)
        att_lst=bId_attriIdx[busiId]
        for att in att_lst:
            attriId_stats[att]+=weightage
        ct+=1
        if (ct%10000)==0:
            print(ct)
#    print(attriId_stats)
    attri_stats={}
    idx_stats={}
    for attri in attri_idx:
        idx=attri_idx[attri]
        attri_stats[attri]=attriId_stats[idx]
        idx_stats[idx]=attriId_stats[idx]
    print(attri_stats)
    print(idx_stats)
    print(attri_idx)
    save_pickle('./pre_data/attriId_popularity.pkl',idx_stats)
    make_plot_data(attri_stats,15,'attribute_popularity','Attribute','Frequency')
    
def make_plot_data(stats,num,filename,x_axis,y_axis):
    cat_lst=sorted(stats,key=stats.get,reverse=True)
    freq=[]
    cat_lst=cat_lst[:num]
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
    for cat in cat_lst:
        f.write(str(cat)+' '+str(stats[cat])+'\n')
    f.close()
    plt.clf()
    
    
def get_user_preferred_attribute():
    num_attri=len(attri_idx.keys())
    print(num_attri)
    bId_attriIdx=load_pickle('./pre_data/businessId_true_Attribute_lst.pkl')
    user_attrLst={}
    attr_user_preferred={}
    attr_user_preferred=defaultdict(lambda:0,attr_user_preferred)
    ct=0
    for user in user_business_review:
        bus_lst=list(user_business_review[user].keys())
#        print(bus_lst)
        attr_true={}
        attr_true=defaultdict(lambda:0,attr_true)
        lst=[]
        for bus in bus_lst:
            attr_lst=bId_attriIdx[bus]
#            print(bus,attr_lst)
            for attr in attr_lst:
                attr_true[attr]=1
        for i in range(num_attri):
           lst.append(attr_true[i])
           attr_user_preferred[i]+=attr_true[i]
        user_attrLst[user]=lst
        ct+=1
        if(ct%100000==0):
            print(ct)
#    print(user_attrLst)
#    print(attr_user_preferred)
    attr_preference={}
    for attr in attri_idx:
        idx=attri_idx[attr]
        attr_preference[attr]=attr_user_preferred[idx]
    
    save_pickle('user_AttributePreferredLst.pkl',user_attrLst)
    make_plot_data(attr_preference,15,'user_attribute_preference','Attribute','Preference')
#        print(lst)
       
def main():
    get_attribute_popularity()   
    get_user_preferred_attribute()
    
    
if __name__=='__main__':
    main()
    
#dic={'tours': 20118, 'breweries': 58503, 'pizza': 341712, 'restaurants': 3654796, 'food': 1158121, 'hotels': 489546, 'travel': 290535}
#lst=['restaurants', 'food', 'hotels', 'pizza', 'travel', 'breweries', 'tours']
#aa=[dic[lst[0]]]
#var_lst=[]
#for l in lst[1:]:
#    aa.append(dic[l])
#    var_lst.append(np.var(aa))
#index=np.arange(len(aa))
#plt.bar(index, aa)
#plt.xlabel('Attributes', fontsize=10)
#plt.ylabel('Count', fontsize=10)
#plt.xticks(index, lst, fontsize=8, rotation=90)
#plt.tight_layout()
#plt.savefig('attribute_selection.png')