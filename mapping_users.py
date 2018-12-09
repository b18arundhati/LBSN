import numpy as np

l = []
friend_pairs = np.load('./pre_data/valid_friend_pairs.npy')
for p in friend_pairs:
	if p[0] not in l:
		l.append(p[0])
	if p[1] not in l:
		l.append(p[1])
l.sort()
with open('./pre_data/mapping_users_for_VERSE.txt','a') as f:
	for i,v in enumerate(l):
		f.write(str(i)+' '+str(v)+'\n')
