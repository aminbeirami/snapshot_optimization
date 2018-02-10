import matplotlib.pyplot as pl
import numpy as np
rec_no = []
time_cost_dyn = []
time_cost_rec = []
query_list = []
single_snap_cost = []
def dyn_vs_rec():
	with open ("data/dynamic.txt") as f:
		for line in f:
			fields = line.split(',')
			rec_no.append(fields[0])
			time_cost_dyn.append(fields[1])
	f.close()
	with open("data/recursive.txt") as p:
		for line in p:
			fields = line.split(',')
			time_cost_rec.append(fields[1])
	p.close()
	pl.figure(facecolor = 'white')
	pl.plot(rec_no,time_cost_dyn,'k--',label ='dynamic',linewidth=1.5)
	pl.plot(rec_no,time_cost_rec,'k',label = 'recursive',linewidth = 1)

	pl.xlabel('numbre of queries')
	pl.ylabel('elapsed time (sec)')
	legend = pl.legend(loc='upper left')
	for label in legend.get_lines():
	    label.set_linewidth(1.5) 
	# pl.legend()
	pl.savefig('graphs/timecost.png', bbox_inches='tight')

def single_snap():
	with open("data/queries.txt") as f:
		for line in f:
			query_list.append(line)
	f.close()
	Q = np.array(query_list)
	with open ("data/single_snap.txt") as p:
		for line in p:
			single_snap_cost.append(line)
	p.close()
	pl.figure(facecolor = 'white')
	pl.ylim([-10,50])
	pl.plot(Q,np.zeros(Q.shape),'k*',label = 'query positions')
	pl.plot(query_list,single_snap_cost,'k--',label = 'cost line' )
	pl.xlabel('timeline')
	pl.ylabel('cost(unit?)')
	legend = pl.legend(loc='upper left')
	pl.savefig("graphs/single_snap_cost.png",bbox_inches = 'tight')
print 'visualizing....'
dyn_vs_rec()
single_snap()
print 'visualization completed successfully.'
