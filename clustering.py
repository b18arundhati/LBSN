import pickle as pkl
# import matplotlib
# matplotlib.use('agg')
# import matplotlib.pyplot as plt
# import sys
# import sklearn
# from sklearn.cluster import KMeans
# import numpy as np
# import copy

with open('./pre_data/user_business_review_morethan5businessperuser.pkl', 'rb') as f:
	data = pkl.load(f)

#plot distribution of users over number of businesses
# stats = {}
# for k in data.keys():
# 	cnt = len(data[k].keys())
# 	if cnt not in stats.keys():
# 		stats[cnt] = 1
# 	else:
# 		stats[cnt] += 1

# for k in stats.keys():
# 	stats[k] = np.log10(stats[k])

# print stats
# # sys.exit(0)
# plt.plot(np.array(stats.keys()), np.array(stats.values()))#, 0.8, color='g')
# plt.xlabel('Number of businesses reviewed')
# plt.ylabel('Number of users')
# plt.show()
# plt.savefig('user_business_histogram.png')
#sys.exit(0)
#cluster for each user, provided number of businesses reviewed by that user > 2
with open('./pre_data/businessId_lat_long.pkl', 'rb') as f:
	loc = pkl.load(f)

# user_dict = copy.deepcopy(data)

# for user in data.keys():
# 	if len(data[user].keys()) <= 5:
# 		user_dict.pop(user)

# print('final number of users: ',len(user_dict.keys())) #final number of users:  208160

# with open('./pre_data/user_business_review_morethan5businessperuser.pkl','wb') as f:
# 	pkl.dump(user_dict, f)



for user in data.keys():

	coords = []

	for business in data[user].keys():
		coords.append(loc[business])

	#find dbindex
	for i in range(2,8):




# coords = []
# for business in data[user].keys():
# 	coords.append(loc[business])

# #cluster
# try:
# 	kmeans = KMeans(n_clusters=2).fit(np.array(coords))
# except Exception as e:
# 	print('couldnot calculate kmeans for user: ',str(user))
# 	continue

# labels = kmeans.labels_

# size_grp1 = np.sum(labels)
# size_total = len(coords)

# if (size_grp1 >= 0.8*size_total) or ((size_total - size_grp1) >= 0.8*size_total):
# 	print user, data[user]

# 	plt.gcf().clear()
# 	x_coords = [t[0] for t in coords]
# 	y_coords = [t[1] for t in coords]
# 	plt.scatter(x_coords,y_coords,c=labels)
# 	plt.show()
# 	plt.savefig('./clusters/cluster_userid_'+str(user)+'.png')

