import pickle
import os
import json
import ast
import numpy as np  
import collections
from collections import defaultdict
import matplotlib.pyplot as plt
from constants import *

def make_plot_data(stats,num,filename,x_axis,y_axis):
    cat_lst=sorted(stats,key=stats.get,reverse=True)
    freq=[]
    cat_lst=cat_lst[:num]
    max_freq=float(stats[cat_lst[0]])
    cat_lst=cat_lst[1:]
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


def load_pickle(filename):
    file=open(filename,'rb')
    object_file=pickle.load(file)
    return object_file
def save_pickle(filename,fileobject):
    filehandler=open(filename,"wb")
    pickle.dump(fileobject,filehandler)
    filehandler.close()

dic={}
with open('./pre_data/category_frequency.txt') as f:
    for i in range(20):
        l=f.readline()
        print(l)
        x=l.strip().split()
        print(x)
        dic[' '.join(x[:-1])]=int(x[-1])
make_plot_data(dic,10,'test','frequency','categories')
    

#dic={}
#dic=defaultdict(lambda:0,dic)
#data=load_pickle('./pre_data/user_business_review.pkl')
#summ=0
#for u in data:
#    dic[len(data[u].keys())]+=1
#print(dic[10],dic[100])
#print(max(dic.keys()))
##    summ+=len(data[u].keys())
##print(dic)
#print(data[2])
#print(len(dic.keys()))
#k=sorted(dic.keys())
#k=k[:100]
#freq=[]
#for kk in k:
#    freq.append(dic[kk])
#print(k,freq)
#plt.plot(k, freq)
#plt.xlabel('No. of reviews', fontsize=10)
#plt.ylabel('No.of users', fontsize=10)
##plt.xticks(index, cat_lst, fontsize=8, rotation=90)
##plt.tight_layout()
#plt.savefig('./pre_data/'+'user_activity.png')
#plt.clf()
#
#print(summ)


#data=load_pickle('./pre_data/friend_list.pkl')
#dic={}
##print(data)
#dic=defaultdict(lambda:0,dic)
#for b in data:
#    cat=data[b]
#    dic[len(cat)]+=1
#print(len(data.keys()))
#print(dic)
#cat_lst=sorted(dic,key=dic.get,reverse=True)
#for c in cat_lst[:20]:
#    print(c,dic[c])
##f=open('./pre_data/Category_frequency.txt')
##d=f.readlines()
##print(len(d))
#
#make_plot_data(dic,10,'num_friend_user','Number of friends','Number of users')

#business_user_review.pkl
#business_user_tipID.pkl