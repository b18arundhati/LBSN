#from __future__ import division
import pickle
import numpy as np
from scipy.spatial import distance
#import population_characteristic_analysis
from operator import itemgetter
import sys

def load_pickle(filename):
    file=open(filename,'rb')
    object_file=pickle.load(file)
    return object_file

def save_pickle(filename,fileobject):
    filehandler=open(filename,"wb")
    pickle.dump(fileobject,filehandler)
    filehandler.close() 

def get_cat_overlap(a,b):
    
    cat_a=user_bus_cat[a]
    cat_b=user_bus_cat[b]
    
    score=len(list(set(cat_a).intersection(set(cat_b))))
    score=float(score)/(max(min(len(cat_a),len(cat_b)),1))
   # print(cat_a,cat_b,score)
    return score

def get_att_overlap(a,b):
    num=len(a)
    A=[]
    B=[]
    for i in range(num):
        if a[i]>0:
            A.append(i)
        if b[i]>0:
            B.append(i)
    score=len(list(set(A).intersection(set(B))))
    score=float(score)/(max(min(len(A),len(B)),1))
    return score
    
def get_bias_score(a,b):
    if user_bias[a]==user_bias[b]:
        return 1
    return 0 
'''
friend_list = load_pickle('./pre_data/friend_list.pkl')
user_location = load_pickle('./pre_data/user_location.pkl')

uids = list(user_location.keys())
pairs = []

ids = list(friend_list.keys())
for i in ids:
  if i not in uids:
    continue
  friends = friend_list[i]
  for f in friends:
    if f == -1:
      continue
    if f not in uids:
      continue
    pairs.append((i,f))

np.save('./pre_data/valid_friend_pairs.npy',np.array(pairs))
print('done')
sys.exit(0)
'''
#for users under consideration, get their complete friends list
#selected_friends=np.load('./pre_data/selected_friend_pairs.npy')
friend_pairs = np.load('./pre_data/valid_friend_pairs.npy')
friends = {}
for i in range(friend_pairs.shape[0]):
  f1 = friend_pairs[i][0]
  f2 = friend_pairs[i][1]
  
  if f1 not in friends:
    friends[f1] = []
  if f2 not in friends:
    friends[f2] = []
  if f2 not in friends[f1]:  
    friends[f1].append(f2)
  if f1 not in friends[f2]:
    friends[f2].append(f1)
  
friends_ids = list(friends.keys())
friends_ids.sort()

user_location=load_pickle('./pre_data/user_location.pkl')
user_att=load_pickle('./pre_data/user_AttributePreferredLst.pkl')
user_bus_cat=load_pickle('./pre_data/userId_businessCategoryList.pkl')
user_bias=load_pickle('./pre_data/userId_bias.pkl')

friends_with_ranking = {}
for id in friends_ids:
  f = friends[id]
  ranking = []
  for f_id in f:
    dist=distance.euclidean(user_location[id],user_location[f_id])
    cat = get_cat_overlap(id, f_id)
    att = get_att_overlap(user_att[id],user_att[f_id])
    bias = get_bias_score(id,f_id)
    score = (dist + cat + att + bias)/np.sqrt((dist**2)+(cat**2)+(att**2)+(bias**2))
    ranking.append((f_id, score))
  ranking = sorted(ranking, key=itemgetter(1))
  friends_with_ranking[id] = ranking
  
save_pickle('./pre_data/userwise_friends_ranking.pkl',friends_with_ranking)


  
    
    
  
