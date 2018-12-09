from constants import *
from collections import defaultdict
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
import pickle
import matplotlib.pyplot as plt
#import math
#import os
import numpy as np
import json
#from scipy import stats
#import matplotlib.pyplot as plt
#from constants import *

def load_pickle(filename):
    file=open(filename,'rb')
    object_file=pickle.load(file)
    return object_file

def save_pickle(filename,fileobject):
    filehandler=open(filename,"wb")
    pickle.dump(fileobject,filehandler)
    filehandler.close() 
    
def review_sentiment_score():
    reviews=load_pickle('./preprocessing/pre_data/reviewId_text.pkl')
    sid = SentimentIntensityAnalyzer()
    review_sentiment={}
    i=0
#    t=0
    for Id in reviews:
    #    print('--------')
        text=reviews[Id]
#        print(text)
        res=sid.polarity_scores(text)
        review_sentiment[Id]=res
#        f=open('test.txt','w')
#        if (res['pos']<res['neg']+0.05) and (res['pos']>res['neg']):
#                print('--------')
#                f.write("=============")
#                print(text)
#                print(str(res))
#                print(text)
#                print(res)
#                t+=1
#        if t>20:
#            break
        
        i+=1
        if(i%10000)==0:
            print(i)
    #        
    save_pickle('./results/reviewId_sentiment.pkl',review_sentiment)
    print('review analysis done for '+str(len(review_sentiment.keys()))+' reviews.')
    

def review_sentiment_classification():
    review_sentiment=load_pickle('./results/reviewId_sentiment.pkl')
    i=0
    review_sentiment_val={}
    data={}
    data=defaultdict(lambda:0,data)
    for rev in review_sentiment:
        res=review_sentiment[rev]
        if res['neg']>res['pos']:
            val=-1
        elif res['pos']>res['neg']+0.025:
            val=1
        else:
            val=0
        review_sentiment_val[rev]=val
        data[val]+=1
        i+=1
        if(i%100000)==0:
            print(i)
    
    dic={}
    dic=defaultdict(lambda:0,dic)
    mapping={0:'neutral',1:'positive',-1:'negative'}
    for id_ in review_sentiment_val:
        dic[mapping[review_sentiment_val[id_]]]+=1
    print(dic)
    print(data)
    make_plot_data(dic,'review_calssification','Review sentiment deduced','Count')
    
    #    print('--------')
#        text=reviews[Id]
    ##    print(text)
    #    text=text.replace('\n','.').replace('  ',' ')
    #    text=text.replace('..','.').replace('. .','.').replace('..','.').replace("'",'').replace('"','')
    #    lines=text.split('.')
    #    try:
    #        lines.remove('')
    #    except:
    #        pass
    #    score=[]
    #    score1=[]
    #    score2=[]
    #    words=0
    #    for lin in lines:
    #        ss = sid.polarity_scores(lin)
    #        score.append(ss['compound'])
    #        score1.append(ss['neg']*len(lin.split()))
    #        score2.append(ss['pos']*len(lin.split()))
    #        words+=len(lin.split())
    #    print(np.sum(score1)/words)
    #    print(np.sum(score2)/words)
        
    #    print(np.mean((score)))
    #    print(np.mean((score2)))
    #    print(sid.polarity_scores(text))
#        res=sid.polarity_scores(text)
    #    if(abs(res['neg']-res['pos'])<0.1):
    #        print(text)
    #        print(res)
    #    if val==0:
    #        print(text)
    #        print(val,res)
    #        i-=1
    #        if i==0:
    #            break
#        review_sentiment[Id]=res
    #        
    save_pickle('./results/reviewId_sentiment_classification.pkl',review_sentiment_val)
    print('review classification done for '+str(len(review_sentiment_val.keys()))+' reviews.')
        
def user_bias():
    user_history=load_pickle('./pre_data/user_business_review.pkl')
    review_classification=load_pickle('./results/reviewId_sentiment_classification.pkl')
    user_bias={}
    num_user=0
    xx=[]
    num_reviews={}
    num_reviews=defaultdict(lambda:0,num_reviews)
#    num_bias_pos=np.zeros(9)
#    num_bias_neg=np.zeros(9)
#    num_bias_neu=np.zeros(9)
    
    ratios=[0.3]#,0.35,0.4,0.45,0.5,0.55, 0.6 , 0.65, 0.7]
    i=0
    for user in user_history:
        reviews=user_history[user]
        review_lst=[]
        for bis in reviews:
            for rev in reviews[bis]:
                try:
                    review_lst.append(review_classification[rev])
                except:
                    continue
        if len(review_lst)>=1:
            num_reviews[len(review_lst)]+=1
            xx.append(len(review_lst))
            pos=len(np.where(np.array(review_lst)==1)[0])
            neg=len(np.where(np.array(review_lst)==-1)[0])
#            if -1 in review_classification:
#                print(review_classification)
            for j in range(1):
                ratio=ratios[j]
                if pos>=(1-ratio)*neg/ratio:
#                    num_bias_pos[j]+=1
                    bias=+1
                elif neg>=(1-ratio)*pos/ratio:
#                    num_bias_neg[j]+=1
                    bias=-1
                else:
#                    num_bias_neu[j]+=1
                    bias=0
#                if bias:
#                    num_bias+=1
            user_bias[user]=bias
            num_user+=1
        i+=1
        if (i%100000==0):
            print(i)
    print('For ratios as '+str(ratios))
#    print('no. of pos biased users are: '+str(num_bias_pos))
#    print('no. of neg biased users are: '+str(num_bias_neg))
#    print('no. of neutral biased users are: '+str(num_bias_neu))
    print('total users are: '+str(len(user_history.keys())))
    print('Bias status for '+str(num_user))
    save_pickle('./results/userId_bias.pkl',user_bias)
#    x=[]
#    y=[]
#    count_reviews=sorted(num_reviews,key=num_reviews.get,reverse=True)
#    for count in count_reviews[:20]:
#        x.append(count)
#        y.append(num_reviews[count])
#    print(num_reviews)
#    print(max(count_reviews))
#    print('.........')
#    print(x)
#    print(y)
#    plt.semilogx(x, y)
#    plt.title('Number of users vs Number of reviews')  
#    plt.ylabel('Number of users')
#    plt.xlabel('Number of reviews')
    xx=[x for x in xx if x<51]
    n, bins, patches = plt.hist(xx, 50, normed=1, facecolor='blue', alpha=0.75)
    plt.xlabel('Number of reviews')
    plt.ylabel('Number of users')
    plt.savefig('./pre_data/'+'num_review_user_stats'+'.png')
    plt.clf()
#    make_plot_data(num_reviews,'num_users_num_reviews','Number of reviews','Number of users')
    
def make_plot_data(stats,filename,x_axis,y_axis):
    cat_lst=sorted(stats,key=stats.get,reverse=True)
    freq=[]
    cat_lst=cat_lst[:20]
    max_freq=float(sum(stats.values()))
    print(max_freq)
    for cat in stats:#['negative','neutral','positive']:
        freq.append(stats[cat]/max_freq)
#    print(freq)
    index = np.arange(len(cat_lst))
    plt.bar(index, freq,align='center')
    plt.xticks(index, cat_lst,  rotation=0)
    plt.ylabel(y_axis, fontsize=15)
    plt.ylim(top=1.0)
    plt.xlabel(x_axis,fontsize=15)
    plt.savefig('./pre_data/'+filename+'.png')
    f=open('./pre_data/'+filename+'.txt','w')
    for cat in cat_lst:
        f.write(str(cat)+' '+str(stats[cat])+'\n')
    f.close()
    plt.clf()
def user_bias_plot():
    data=load_pickle('./results/userId_bias.pkl')
    dic={}
    dic=defaultdict(lambda:0,dic)
    mapping={0:'neutral',1:'positive',-1:'negative'}
    for id_ in data:
        dic[mapping[data[id_]]]+=1
    print(dic)
    make_plot_data(dic,'user_biasness','Biased sentiment deduced','Count')
        
        

if __name__=='__main__':
#        review_sentiment_score()
        review_sentiment_classification()
#    user_bias()
#    user_bias_plot()
        