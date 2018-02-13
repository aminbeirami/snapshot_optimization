from time import time, sleep
import numpy as np
import progressbar
import math
import os

cost_table_dyn = []

def fetch_snap_no():
    with open('data/snap_no.txt') as f:
        for i in f:
            return int(i)

def make_queries(n):
    Q = np.vstack([
        np.random.normal(4, 4, (n, 1)),
        np.random.normal(40, 4, (n, 1)),
        np.random.normal(60,4,(n,1))
        ])
    a, b = np.min(Q), np.max(Q)
    Q = np.vstack([Q, np.random.uniform(a, b, (10, 1))])
    Q = Q - np.min(Q)
    return np.squeeze(Q)

def fetch_queries():
    queries = []
    with open('data/queries.txt') as f:
        for items in f:
            queries.append(float(items.translate(None,'\n')))
    f.close()
    return queries

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

def calc_cost(Q,cut):
    if cut >0:
        Q = Q[-cut:]
        cost = calc_single_cost(Q)
        return cost
    else:
        return 0

def init_cost_tables(no_snap,size_queries):
    init_val = -1
    for j in range (no_snap+1):
        for i in range(size_queries+1):
            cost_table_dyn[j][i] = init_val


def init_first_row(Q,size_queries):
    for i in range(1,size_queries+1):
        queries = Q[:i]
        cost_table_dyn[1][i] = calc_single_cost(queries)


def dynamic_cost(Q,no_snap,size_queries):
    init_first_row(Q,size_queries)
    for j in range(2,no_snap+1):
        for i in range(1,size_queries+1):
            min_value = np.inf
            for k in range(1,i+1):
                current_cost = cost_table_dyn[j-1][k]+calc_cost(Q[:i],(i-k))
                if current_cost < min_value:
                    min_value = current_cost
            cost_table_dyn[j][i] = min_value


def recursive_cost(Q,no_snap):
    if (no_snap == 1) or (len(Q) == 1):
        return calc_single_cost(Q)
    else:
        min_value = np.inf
        for i in range(0,len(Q)):
            min_value = min(min_value, calc_single_cost(Q[:i])+recursive_cost(Q[i:],no_snap-1))
        return min_value


print 'started examining the cost for fixed snapshots but various queries.'
snapshot_no = fetch_snap_no()
bar = progressbar.ProgressBar(maxval=50, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
for i in range (1,20,2):
    query_list = sorted(make_queries(i))
    query_size = len(query_list)
    cost_table_dyn = np.zeros((snapshot_no+1,query_size+1))
    init_cost_tables(snapshot_no,query_size)
    duration = timeit(dynamic_cost,query_list,snapshot_no,query_size)
    save_file_time(query_size,duration,'dynamic_multiquery')
    duration = 0;
    duration = timeit(recursive_cost,query_list,snapshot_no)
    save_file_time(query_size,duration,'recursive_multiquery')
    bar.update(i)
    sleep(0.1)
bar.finish()

print "test finished successfully."

print 'started examining fixed number of queries with various number of snapshots'
snapshot_no = fetch_snap_no()
bar = progressbar.ProgressBar(maxval=5, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
for i in range(1,5):
    duration = 0
    query_list = sorted(fetch_queries())
    query_size = len(query_list)
    cost_table_dyn = np.zeros((i+1,query_size+1))
    init_cost_tables(i,query_size)
    duration = timeit(dynamic_cost,query_list,i,query_size)
    save_file_time(i,duration,'dynamic_multisnap')
    duration = 0
    duration = timeit(recursive_cost,query_list,i)
    save_file_time(i,duration,'recursive_multisnap')
    bar.update(i)
    sleep(0.1)
bar.finish()
print 'Completed!'