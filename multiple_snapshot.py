import numpy as np
import matplotlib.pyplot as pyplot
import math
from time import time

cost_table_dyn = []

def fetch_queries():
    queries = []
    with open('data/queries.txt') as f:
        for items in f:
            queries.append(float(items.translate(None,'\n')))
    f.close()
    return queries

def fetch_snap_no():
    with open('data/snap_no.txt') as f:
        for i in f:
            return int(i)


def save_file_queries(Q):
    f = open("data/queries.txt","a+")
    for i in range(len(Q)):
        f.write(str(Q[i])+"\n")
    f.close()

def save_multiple_cost(cost_table,snapshot_no,query_size):
    f = open("data/individual_cost.txt","a+")
    for i in range(1,snapshot_no+1):
        f.write(str(i)+","+str(cost_table[i][query_size])+"\n")
    f.close()
def save_overall_cost(cost):
    f = open("data/overall_cost.txt","w+")
    f.write("optimal,"+str(cost)+'\n')
    f.close()

def cost_array(Q,snap_pos,name):
    cost = []
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
print "calculating overall cost ..."

query_list = sorted(fetch_queries())
snapshot_no = fetch_snap_no()
save_file_queries(query_list)
query_size = len(query_list)
cost_table_dyn = np.zeros((snapshot_no+1,query_size+1))
init_cost_tables(snapshot_no,query_size)
dyn_cost = dynamic_cost(query_list,snapshot_no,query_size)
rec_cost = recursive_cost(query_list,snapshot_no)
save_multiple_cost(cost_table_dyn,snapshot_no,query_size)
save_overall_cost(cost_table_dyn[snapshot_no][query_size])


print "the cost of dynamic for "+str(snapshot_no)+ " snapshot = " + str(cost_table_dyn[snapshot_no][query_size])
print "the cost of recursive for "+str(snapshot_no)+ " snapshot = " + str(rec_cost)
