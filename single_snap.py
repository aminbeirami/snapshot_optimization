import numpy as np
import matplotlib.pyplot as pyplot

def fetch_queries():
	queries = []
	with open('data/queries.txt') as f:
		for items in f:
			queries.append(float(items.translate(None,'\n')))
	f.close()
	return queries

def make_snapshots(Q):
    a, b = np.min(Q), np.max(Q)
    snapshot =  np.random.uniform(a, b, 2)
    return snapshot

def time_cost(Q, S):
    S = np.array(S)
    nQ = Q.shape[0]
    nS = S.shape[0]
    d = np.zeros((nQ, nS))
    for i in range(nQ):
        q = Q[i]
        d[i, :] = np.abs(S - q)
    c = np.min(d, axis=1)
    return np.sum(c)

def plot_k1(Q):
	Q = np.array(Q)
	med = np.median(Q)
	tmax = np.max(Q)
	ts = np.linspace(0, tmax, 100)
	cost = [time_cost(Q, [s]) for s in ts]
	pyplot.figure()
	pyplot.ylim([-50,max(cost)+200])
	pyplot.plot(Q, np.zeros(Q.shape), 'k*',label = 'queries')
	pyplot.plot(ts, cost, 'k--', label = 'overal cost')
	pyplot.plot(med,np.zeros(med.shape),"o",label = 'median of queries',color = 'red')
	pyplot.xlabel('timeline')
	pyplot.ylabel('cost')
	legend = pyplot.legend(loc='upper left')
	pyplot.savefig('graphs/single.png',bbox_inches = 'tight')


Q = fetch_queries()
S = make_snapshots(Q)

plot_k1(Q)