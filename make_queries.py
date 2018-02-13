import numpy as np
SNAPSHOT_NO = 4
def make_queries():
    Q = np.vstack([
        np.random.normal(4, 4, (20, 1)),
        np.random.normal(20, 4, (20, 1)),
        np.random.normal(40, 4, (20, 1))
        ])
    a, b = np.min(Q), np.max(Q)
    Q = np.vstack([Q, np.random.uniform(a, b, (10, 1))])
    Q = Q - np.min(Q)
    return np.squeeze(Q)

def save_file_queries(Q):
    f = open("data/queries.txt","a+")
    for i in range(len(Q)):
        f.write(str(Q[i])+"\n")
    f.close()

def save_snap_no():
	f = open("data/snap_no.txt","w+")
	f.write(str(SNAPSHOT_NO))
	f.close()
query_list = make_queries()
save_file_queries(query_list)
save_snap_no()