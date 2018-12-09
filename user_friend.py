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
    
    

json_data=open(os.path.join(data_folder,user_json))
user_id={}
id_user={}
user_friends={}
user_count=0
while True:
    try:
        line=json_data.readline()
        line_dict=json.loads(line.strip())
#        print(line_dict)
        user_name=line_dict["user_id"]
        user_id[user_name]=user_count
        id_user[user_count]=user_name
        user_count+=1
        if user_count%100000==0:
            print(user_count)
        user_friends[user_name]=line_dict["friends"]
    except:
        break
print(user_count)
print(len(user_id.keys()))
user_friends_id={}   
friend_new=[]   
for user in user_friends:
    if user_friends[user]=='None':
        user_friends_id[user_id[user]]=[]
    else:
        friends=user_friends[user].split(',')
        friend_lst=[]
        flag=1
        for friend in friends:
            try:
                friend_id=user_id[friend.strip()]
                friend_lst.append(friend_id)
            except:
                friend_lst.append(-1)
                friend_new.append(friend)
                continue
        user_friends_id[user_id[user]]=friend_lst
#        print(user_friends[user])
#        print(type(user_friends[user]))
#        print(user_friends[user].split(','))
print('New users in friend list = '+str(len(set(friend_new))))      
save_pickle('./pre_data/id_user_mapping.pkl',id_user)
save_pickle('./pre_data/user_id_mapping.pkl',user_id)
save_pickle('./pre_data/friend_list.pkl',user_friends_id)

#1518169- data we have is for these users
#12593281- in friend list but not in data
