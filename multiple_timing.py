from time import time, sleep
import numpy as np
import progressbar
import math
import os

SNAPSHOT_NO = 3
QUERY_SIZE = 0
cost_table_dyn = []

def make_queries(n):
    Q = np.vstack([
        np.random.normal(4, 4, (n, 1)),
        np.random.normal(40, 4, (n, 1))
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

def save_file_time(query_no,duration,name):
    f = open("data/"+name+'.txt','a')
    f.write(str(query_no)+','+str(duration)+'\n')
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
            # cost_table_rec[j][i] = 0

def init_first_row(Q,size_queries):
    for i in range(1,size_queries+1):
        queries = Q[-i:]
        cost_table_dyn[1][i] = calc_single_cost(queries)

def dynamic_cost(Q,no_snap,size_queries):
    init_first_row(Q,size_queries)
    for j in range(2,no_snap+1):
        for i in range (1, size_queries+1):
            min_value = np.inf
            for k in range(1,i+1):
                min_value = min(min_value,cost_table_dyn[j-1][k]+calc_cost(Q[-i:],j-1,(i-k)))
                # print "cost_table_dyn["+str(j-1)+"]["+str(k)+"]"+ "+calc_cost(Q[:"+str(i)+"],"+str(j-1)+","+str((i-k))+"))"
            # print "-----------------------------------"            
            cost_table_dyn[j][i] = min_value

def recursive_cost(Q,no_snap):
    if (no_snap == 1) or (len(Q) == 1):
        return calc_single_cost(Q)
    else:
        min_value = np.inf
        for i in range(0,len(Q)):
            min_value = min(min_value, calc_single_cost(Q[:i])+recursive_cost(Q[i:],no_snap-1))
        return min_value



print 'started examining the cost of time for multiple queries.'
bar = progressbar.ProgressBar(maxval=50, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
for i in range (1,50,3):
    query_list = sorted(make_queries(i))
    QUERY_SIZE = len(query_list)
    cost_table_dyn = np.zeros((SNAPSHOT_NO+1,QUERY_SIZE+1))
    init_cost_tables(SNAPSHOT_NO,QUERY_SIZE)
    duration = timeit(dynamic_cost,query_list,SNAPSHOT_NO,QUERY_SIZE)
    save_file_time(QUERY_SIZE,duration,'dynamic')
    duration = 0;
    duration = timeit(recursive_cost,query_list,SNAPSHOT_NO)
    save_file_time(QUERY_SIZE,duration,'recursive')
    bar.update(i)
    sleep(0.1)
bar.finish()
print 'Completed!'