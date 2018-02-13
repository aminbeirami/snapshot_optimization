import numpy as np
from random import randint

def fetch_snap_no():
    with open('data/snap_no.txt') as f:
        for i in f:
            return int(i)

def fetch_queries():
	queries = []
	with open('data/queries.txt') as f:
		for items in f:
			queries.append(float(items.translate(None,'\n')))
	f.close()
	return queries

def save_cost(regular,random):
	f = open("data/overall_cost.txt","a")
	f.write("regular,"+str(regular)+"\n")
	f.write("random,"+str(random)+"\n")

def regular_snapshot(Q,snapshot_no):
	query_slices = []
	query_len = len(Q)
	cut_size = query_len/snapshot_no
	for i in range(snapshot_no-1):
		query_slices.append(Q[:cut_size])
		Q = Q[cut_size:]
	query_slices.append(Q)
	return query_slices

def random_snapshot(Q,snapshot_no):
	query_slices = []
	random_cut = 0
	for i in range(snapshot_no-1):
		query_len = len(Q)
		random_cut = randint(1,query_len-1)
		query_slices.append(Q[:random_cut])
		Q = Q[random_cut:]
	query_slices.append(Q)
	return query_slices

def calc_slice_cost(arr,snap):
	cost = 0
	for i in range(len(arr)):
		cost+=abs(arr[i]-snap)
	return cost
def overall_cost(slices):
	snap_pos = 0
	cost = 0
	for i in range(len(slices)):
		snap_pos = np.median(slices[i])
		cost += calc_slice_cost(slices[i],snap_pos)
	return cost

query_list = fetch_queries()
snapshot_no = fetch_snap_no()
regular_slices = regular_snapshot(query_list,snapshot_no)
regular_cost = overall_cost(regular_slices)
random_slices = random_snapshot(query_list,snapshot_no)
random_cost = overall_cost(random_slices)
save_cost(regular_cost,random_cost)
