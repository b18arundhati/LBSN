from collections import defaultdict
import pickle
from scipy.spatial import distance
import numpy as np
import matplotlib.pyplot as plt

def load_pickle(filename):
    file=open(filename,'rb')
    object_file=pickle.load(file)
    return object_file

def save_pickle(filename,fileobject):
    filehandler=open(filename,"wb")
    pickle.dump(fileobject,filehandler)
    filehandler.close() 
    
friend_data=load_pickle('./pre_data/friend_list.pkl')
friend_pair_dic={}
NUM=50000
user_location={}
user_att=load_pickle('./pre_data/user_AttributePreferredLst.pkl')
user_bus_cat=load_pickle('./pre_data/userId_businessCategoryList.pkl')
user_bias=load_pickle('./pre_data/userId_bias.pkl')
def get_user_with_loc():
    f=open('./../results_user_business_clustering/business_locations_kgeq5.out')
    while True:
        data=f.readline()
        if not data:
            break
        [id_,locx,locy]=data.strip().replace(':',' ').replace(',',' ').split()
        user_location[int(id_)]=[float(locx),float(locy)]
    save_pickle('./pre_data/user_location.pkl',user_location)
    print('got user locations. values=',len(user_location.keys()))

def get_user_lst():
    user_location=load_pickle('./pre_data/user_location.pkl')
    friends=friend_data.keys()
    atts=user_att.keys()
    cats=user_bus_cat.keys()
    bias=user_bias.keys()
    locs=user_location.keys()
    locs=list(locs)
    print(665937 in locs)
#    print(locs)
    print('------')
    users=set(list(friends)).intersection(set(atts))
    print(len(list(users)))
    users=users.intersection(set(list(cats)))
    print(len(list(users)))
    users=users.intersection(set(list(bias)))
    print(len(list(users)))
    users=list(users.intersection(set(locs)))
    print(len(users))
    return users
 
def get_friend_pairs(users):
    friend_pair=[]
#    ct=0
    print('#users = ',len(users))
    print('#users with locations = ',len(user_location.keys()))
    for user in users:
#        print(user)
        friends=friend_data[user]
        friends=[x for x in  friends if (x>-1)]
        friends=[x for x in  friends if (x>user)]
        for friend in friends:
            if friend not in users:#user_location:
                continue
#            ct+=1
            
            friend_pair.append((user,friend))
            friend_pair_dic[(user,friend)]=1
#            if ct==10:
#                continue
    friend_pair=np.array(friend_pair)
#    print(friend_pair)
    np.save('./pre_data/possible_friend_pairs.npy',friend_pair)
    
    print(friend_pair.shape)
    num=friend_pair.shape[0]
    print('total friends with both having locations',num)
    idx=np.random.choice(num,NUM,replace=False)
    selected_friends=[]
    for i in idx:
        selected_friends.append(friend_pair[i])
    selected_friends=np.array(selected_friends)
    np.save('./pre_data/selected_friend_pairs.npy',selected_friends)
    print(selected_friends.shape)
def get_non_friend_pairs(users):
#    users=list(user_location.keys())
    num=len(users)
    ct=0
    user_pair={}
    selected_pairs=[]
    while True:
        id_=np.random.choice(num*num,1)[0]
#        print(id_)
        x=users[int(int(id_)/num)]
        y=users[int(int(id_)%num)]
        if x==y:
            continue
        pair=(min(x,y),max(x,y))
#        print(pair)
        if pair in friend_pair_dic:
            continue
        if pair in user_pair:
            continue
        user_pair[pair]=1
        selected_pairs.append(pair)
        ct+=1
        if ct>=NUM:
            break
    selected_pairs=np.array(selected_pairs)
    np.save('./pre_data/selected_non_friend_pairs.npy',selected_pairs)
    print(selected_pairs.shape)

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

def get_stats(data,num,x_axis,y_axis,filename):
    arrf=data['friend']
    arrnf=data['non_friend']
#    print(sum(arrf))
#    print(sum(arrnf))
#    print(data.keys())
    arr=arrf+arrnf
    min_=min(arr)
    max_=max(arr)
    print(min_,max_)
    size=float(max_ - min_)/num
    val1=[]
    val2=[]
    arr1=arrf[:]
    arr2=arrnf[:]
    X1=[]
    X2=[]
    for i in range(num-1,-1,-1):
        bin1=[x for x in arr1 if x>=(min_+(i*size))]
        arr1=[x for x in arr1 if x<(min_+(i*size))]
#        print(len(bin1))
        val1=[len(bin1)]+val1
        bin2=[x for x in arr2 if x>=(min_+(i*size))]
        arr2=[x for x in arr2 if x<(min_+(i*size))]
#        print(len(bin2))
        val2=[len(bin2)]+val2
        X1=[min_+(i*size)+(size/3)]+X1
        X2=[min_+(i*size)+(2*size/3)]+X2
    print(X1,X2)
    print(val1,val2)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1=ax.bar(X1, val1,width=size/3,color='b',align='center')
    rects2=ax.bar(X2, val2,width=size/3,color='g',align='center')
#    plt.hist(arr1, bins=np.linspace(min_,max_,num+1))
    ax.set_xlabel(x_axis, fontsize=5)
    ax.set_ylabel(y_axis, fontsize=5)
    ax.legend( (rects1[0], rects2[0]), ('Friends', 'Non-friends') )
    plt.savefig('./characterizing_users/'+filename+'.png')
#    ax.clf()
    plt.clf()
    
def get_characteristics():
    selected_non_friends=np.load('./pre_data/selected_non_friend_pairs.npy')
    selected_friends=np.load('./pre_data/selected_friend_pairs.npy')
    user_location=load_pickle('./pre_data/user_location.pkl')
    Loc={}
    Bias={}
    Cat={}
    Att={}
    for name,pair_data in zip(['friend','non_friend'],[selected_friends,selected_non_friends]):
        print('yyys')
        loc=[]
        bias=[]
        cat=[]
        att=[]
        for pair in pair_data:
            dist=distance.euclidean(user_location[pair[0]],user_location[pair[1]])
            loc.append(dist)
            cat.append(get_cat_overlap(pair[0],pair[1]))
            att.append(get_att_overlap(user_att[pair[0]],user_att[pair[1]]))
            bias.append(get_bias_score(pair[0],pair[1]))
        Loc[name]=loc
        Bias[name]=bias
        Cat[name]=cat
        Att[name]=att
    print('location')
    get_stats(Loc,10,'distance','count','characteristic_dist')
    print('bias')
    get_stats(Bias,2,'biasness','çount','characteristic_bias')    
    print('çategories')
    get_stats(Cat,10,'Category coeff','çount','characteristic_category')
    print('Attributes')
    get_stats(Att,10,'Attribute coeff','çount','characteristic_att')
        
if __name__=='__main__':
#    get_user_with_loc()
#    users=get_user_lst()
#    get_friend_pairs(users)
#    arr=get_characteristics()
#    get_non_friend_pairs(users)
    get_characteristics()
#    plt.hist(data, bins=np.arange(min(data), max(data) + binwidth, binwidth))
#    plt.hist([0,1,2,3,2,3,4,2,3], bins=[0,1,2,3,4,5,6,7,8])
#    plt.savefig('temp.png')