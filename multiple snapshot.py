import numpy as np
import matplotlib.pyplot as pyplot
import math
SNAPSHOT_NO = 3
QUERY_SIZE = 0
cost_table = []
def make_queries():
    Q = np.vstack([
        np.random.normal(4, 4, (20, 1)),
        np.random.normal(40, 4, (20, 1))
        ])
    a, b = np.min(Q), np.max(Q)
    Q = np.vstack([Q, np.random.uniform(a, b, (10, 1))])
    Q = Q - np.min(Q)
    return np.squeeze(Q)

def calc_single_cost(Q,snap_pos):
    cost = 0.0;
    for i in range(len(Q)):
        cost += abs(Q[i] - snap_pos)
    return cost

def calc_cost(Q,snap_no,cut):
    if snap_no > 0:
        if cost_table[snap_no][cut] > -1: #if the cost was calculated before, don't calculate it again
            return cost_table[snap_no][cut]
        else:
            queries = Q[cut:]
            med = np.median(queries)
            return calc_single_cost(queries,med)

def init_cost_table(no_snap,size_queries):
    init_val = -1
    for j in range (no_snap+1):
        for i in range(size_queries+1):
            cost_table[j][i] = init_val

def init_first_row(Q,size_queries):
    for i in range(1,size_queries+1):
        queries = Q[-i:]
        cost_table[1][i] = calc_single_cost(queries,np.median(queries))

def make_sections(Q,no_snap,size_queries):
    init_first_row(Q,size_queries)
    for j in range(2,no_snap+1):
        for i in range (1, size_queries+1):
            min_value = np.inf
            for k in range(1,i+1):
                min_value = min(min_value,cost_table[j-1][k]+calc_cost(Q[-i:],j-1,(i-k)))
                # print "cost_table["+str(j-1)+"]["+str(k)+"]"+ "+calc_cost(Q[:"+str(i)+"],"+str(j-1)+","+str((i-k))+"))"
            # print "-----------------------------------"            
            cost_table[j][i] = min_value
query_list = sorted(make_queries())
QUERY_SIZE = len(query_list)
cost_table = np.zeros((SNAPSHOT_NO+1,QUERY_SIZE+1))
init_cost_table(SNAPSHOT_NO,QUERY_SIZE)
make_sections(query_list,SNAPSHOT_NO,QUERY_SIZE)
print cost_table
