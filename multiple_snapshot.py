import numpy as np
import matplotlib.pyplot as pyplot
import math
from time import time
SNAPSHOT_NO = 2
QUERY_SIZE = 0
cost_table_dyn = []

def make_queries():
    Q = np.vstack([
        np.random.normal(4, 4, (20, 1)),
        np.random.normal(40, 4, (20, 1)),
        np.random.normal(20, 4, (20, 1))
        ])
    a, b = np.min(Q), np.max(Q)
    Q = np.vstack([Q, np.random.uniform(a, b, (10, 1))])
    Q = Q - np.min(Q)
    return np.squeeze(Q)

def timeit(f, *args):
    start = time()
    f(*args)
    duration = time() - start
    return duration

def save_file_queries(Q):
    f = open("data/queries.txt","a+")
    for i in range(len(Q)):
        f.write(str(Q[i])+"\n")
    f.close()

def cost_array(Q,name):
    cost = []
    snap_pos = np.median(Q)
    f = open("data/"+name+"_snap.txt","a+")
    for i in range(len(Q)):
        cost.append(abs(Q[i]-snap_pos))
    f.write(str(cost) + "|" + str(snap_pos) + "|" + str(max(Q)) + "|" + str(min(Q)) + "\n")
    f.close()

def calc_single_cost(Q):
    if Q == []:
        return 0
    else:
        cost = 0.0;
        snap_pos = np.median(Q)
        for i in range(len(Q)):
            cost += abs(Q[i] - snap_pos)
        return cost

def calc_cost(Q,snap_no,cut):
    if snap_no > 0:
        if cost_table_dyn[snap_no][cut] > -1: #if the cost was calculated before, don't calculate it again
            return cost_table_dyn[snap_no][cut]
        else:
            if cut == 0:
                return 0
            else:
                queries = Q[cut:]
                return calc_single_cost(queries)

def init_cost_tables(no_snap,size_queries):
    init_val = -1
    for j in range (no_snap+1):
        for i in range(size_queries+1):
            cost_table_dyn[j][i] = init_val

def init_first_row(Q,size_queries):
    for i in range(1,size_queries+1):
        queries = Q[-i:]
        cost_table_dyn[1][i] = calc_single_cost(queries)

def slice_the_queries(Q,cut):
    query_slices = []
    for i in range(len(cut)):
        slices = Q[:cut[i]]
        query_slices.append(slices)
        Q = Q[cut[i]:]
    return query_slices
def the_best_cuts(Q,cut):
    multiple_cuts = []
    size = len(Q)
    # cut.reverse()
    cut.append(0)
    for i in range(SNAPSHOT_NO):
        slices = size - cut[i]
        size = cut[i] 
        multiple_cuts.append(slices)
    return multiple_cuts

def dynamic_cost(Q,no_snap,size_queries):
    best_cut = []
    init_first_row(Q,size_queries)
    for j in range(2,no_snap+1):
        for i in range (1, size_queries+1):
            min_value = np.inf
            index = 0
            cut = 0
            for k in range(1,i+1):
                current_cost = cost_table_dyn[j-1][k]+calc_cost(Q[-i:],j-1,(i-k))
                if current_cost < min_value:
                    min_value = current_cost
                    index = j-1
                    cut = i-k
                # print "cost_table_dyn["+str(j-1)+"]["+str(k)+"]"+ "+calc_cost(Q[:"+str(i)+"],"+str(j-1)+","+str((i-k))+"))"
            # print "-----------------------------------"            
            cost_table_dyn[j][i] = min_value
        best_cut.append(cut)
    return best_cut

def recursive_cost(Q,no_snap):
    if (no_snap == 1) or (len(Q) == 1):
        return calc_single_cost(Q)
    else:
        min_value = np.inf
        for i in range(0,len(Q)):
            min_value = min(min_value, calc_single_cost(Q[:i])+recursive_cost(Q[i:],no_snap-1))
        return min_value

query_list = sorted(make_queries())
save_file_queries(query_list)
QUERY_SIZE = len(query_list)
cost_table_dyn = np.zeros((SNAPSHOT_NO+1,QUERY_SIZE+1))
init_cost_tables(SNAPSHOT_NO,QUERY_SIZE)
best_cut = dynamic_cost(query_list,SNAPSHOT_NO,QUERY_SIZE)
cost_array(query_list,'single')
print recursive_cost(query_list,SNAPSHOT_NO)
print best_cut
multiple_cuts = the_best_cuts(query_list,best_cut)
query_slices = slice_the_queries(query_list,multiple_cuts)
for i in range (len(query_slices)):
    cost_array(query_slices[i],'multiple')
# cost_line = 
# print cost_table_dyn
# for i in range(1,SNAPSHOT_NO+1):
#     print "when there is/are "+ str(i)+" snapshots, the minimum possible cost is: "+str(cost_table_dyn[i][QUERY_SIZE])
