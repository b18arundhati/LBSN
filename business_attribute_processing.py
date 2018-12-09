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

json_data=open(os.path.join(data_folder,business_json))
business_user_review=load_pickle('./pre_data/business_user_review.pkl')
business_id=load_pickle('./pre_data/business_id_mapping.pkl')
user_business_review=load_pickle('./pre_data/user_business_review.pkl')

attribute_id={}
attributes_=['bikeparking', 'businessacceptscreditcards', 'businessparking_garage', 
             'businessparking_street', 'businessparking_validated', 'businessparking_lot', 
             'businessparking_valet', 'goodforkids', 'hastv',
            'outdoorseating', 'restaurantsdelivery', 'restaurantsgoodforgroups', 'restaurantsreservations', 
            'restaurantstakeout', 'alcohol', 'caters', 'dogsallowed', 'drivethru', 'restaurantstableservice', 
            'wheelchairaccessible', 'wifi', 'byob', 'byobcorkage', 'coatcheck', 'corkage', 'goodfordancing', 'happyhour', 
            'byappointmentonly', 'acceptsinsurance', 'businessacceptsbitcoin', 
            'restaurantscounterservice', 'open24hours']
att_val_map={'False': 0, 'True': 1, False: 0, True: 1, 'none': 0, 'no': 0, 'beer_and_wine': 1,
              'free': 1,'full_bar': 1, 'yes_free': 1,'paid':1 , 'yes': 1, 'yes_corkage': 1}

businessId_attribute_lst={}

#attribute_stats=collections.defaultdict(dict)
attibute_index={}
for att in attributes_:
    attibute_index[att]=len(attibute_index.keys())
    
def make_plot_data(stats,filename,x_axis,y_axis):
    cat_lst=sorted(stats,key=stats.get,reverse=True)
    freq=[]
    for cat in cat_lst:
        freq.append(stats[cat])
    index = np.arange(len(freq))
    plt.bar(index, freq)
    plt.xlabel(x_axis, fontsize=5)
    plt.ylabel(y_axis, fontsize=5)
    plt.xticks(index, cat_lst, fontsize=5, rotation=90)
    plt.savefig('./pre_data/'+filename+'.png')
    f=open('./pre_data/'+filename+'.txt','w')
    for cat in cat_lst:
        f.write(str(cat)+' '+str(stats[cat])+'\n')
    f.close()
attri_stats={}
attri_stats=defaultdict(lambda:0,attri_stats)
        
def update_attributes(id_,line_dict):
    try:
        
        attributes=line_dict['attributes']
        if not attributes:
            x=1/0#just to raise an error
    except:
        attributes=[]
    att_feat=np.ones(len(attributes_))
    att_feat=-1*att_feat
    attri_stats['total_data']+=1
    for attribute in attributes:
        att=attribute.strip().lower()
        status=attributes[attribute]
        if att in attibute_index:
            att_feat[attibute_index[att]]=att_val_map[status]
            attri_stats[att]+=1
    businessId_attribute_lst[id_]=att_feat
    
#    if id_<10:
#        print(id_,att_feat)
#        print(attributes)
#        print()
#        if(str(status)[0]=='{'):
#            dic=ast.literal_eval(str(status))
#            for k in dic:
#                attr=str(att)+'_'+str(k)
#                attribute_stats[attr][dic[k]]=1
##                
#        else:
#            attribute_stats[att][status]=1
#                
    
business_count=0
while True:
    try:
        line=json_data.readline()
        line_dict=json.loads(line.strip())
        business_name=line_dict["business_id"]
        id_=business_id[business_name]
        update_attributes(id_,line_dict)
        business_count+=1
        if business_count%10000==0:
            print(business_count)
    except:
        break
make_plot_data(attri_stats,'Attribute_frequency','Attribute','We have data for')
#for att in attribute_stats:
#    print(att,attribute_stats[att])
#print(attribute_stats.keys())
print(len(businessId_attribute_lst.keys()))
print(len(attibute_index.keys()))
save_pickle('./pre_data/businessId_attribute_lst.pkl',businessId_attribute_lst)
save_pickle('./pre_data/businessAttribute_index.pkl',attibute_index)