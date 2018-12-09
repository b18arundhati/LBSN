import numpy as np
import pickle
from operator import itemgetter

emb = np.fromfile('friend_pairs.bin', np.float32).reshape(-1, 128)

indices = []

with open('../../preprocessing/pre_data/mapping_users_for_VERSE.txt','r') as f:
	line = f.readline()
	while line != '':
		indices.append(int(line.split()[1].strip()))
		line = f.readline()

friend_pairs = np.load('../../preprocessing/pre_data/valid_friend_pairs.npy')

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

friends_with_ranking = {}
for n,i in enumerate(indices):
	f = friends[i]
	emb_i = emb[n]
	ranking = []
	for frnd in f:
		emb_f = emb[indices.index(frnd)]
		score = np.dot(emb_i, emb_f)
		ranking.append((frnd, score))
	ranking = sorted(ranking, key=itemgetter(1))
	friends_with_ranking[i] = ranking
	print(n)

def save_pickle(filename,fileobject):
	filehandler=open(filename,"wb")
	pickle.dump(fileobject,filehandler)
	filehandler.close()



save_pickle('../../preprocessing/pre_data/userwise_friends_ranking_VERSE.pkl',friends_with_ranking)

