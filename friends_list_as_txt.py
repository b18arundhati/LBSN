import numpy as np

friends = np.load('pre_data/valid_friend_pairs.npy')
pairs_count = friends.shape[0]

for i in range(0, pairs_count):
	print friends[i][0], friends[i][1]


