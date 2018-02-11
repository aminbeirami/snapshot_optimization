import matplotlib.pyplot as pl
import numpy as np

def dyn_vs_rec():
	rec_no = []
	time_cost_dyn = []
	time_cost_rec = []
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

def queries():
	query_list = []
	with open("data/queries.txt") as f:
		for line in f:
			query_list.append(line)
	f.close()
	return query_list

def snap_cost(name):
	snap_cost = []
	snap_pos = []
	maximum = []
	minimum = []
	with open("data/"+name+"_snap.txt") as f:
		for line in f:
			sections = line.split('|')
			costs = sections[0]
			costs = costs.translate(None,'([])')
			snap_cost.append(costs.split(","))
			snap_pos.append(sections[1])
			maximum.append(sections[2])
			minimum.append(sections[3])
	f.close()
	return snap_cost, snap_pos, maximum, minimum

def plot_single_cost():
	single_snap_cost, snap_pos, min_val, max_val = snap_cost('single')
	Q = np.array(queries())
	pl.figure(facecolor = 'white')
	pl.ylim([-10,50])
	pl.plot(Q,np.zeros(Q.shape),'k*',label = 'query positions')
	pl.plot(Q,single_snap_cost[0],'k--',label = 'cost line' )
	pl.plot(snap_pos[0],0,'o',color = 'red', label = 'snapshot position')
	pl.xlabel('timeline')
	pl.ylabel('cost(unit?)')
	legend = pl.legend(loc='upper left')
	pl.savefig("graphs/single_snap_cost.png",bbox_inches = 'tight')

def plot_multiple_cost():
	complete_cost =[]
	multi_snap_cost, snap_pos, min_val, max_val = snap_cost('multiple')
	for i in range(len(multi_snap_cost)):
		complete_cost = complete_cost+multi_snap_cost[i]
	Q = np.array(queries())
	snap_pos = np.array(snap_pos)
	pl.figure(facecolor = 'white')
	pl.ylim([-10,50])
	pl.plot(Q,np.zeros(Q.shape),'k*',label = 'query positions')
	pl.plot(Q,complete_cost,'k--',label = 'cost line' )
	pl.plot(snap_pos,np.zeros(snap_pos.shape),"o",label = 'snapshot position',color = 'red')
	pl.xlabel('timeline')
	pl.ylabel('cost(unit?)')
	legend = pl.legend(loc='upper left')
	pl.savefig("graphs/multi_snap_cost.png",bbox_inches = 'tight')

print 'visualizing....'
dyn_vs_rec()
plot_single_cost()
plot_multiple_cost()
print 'visualization completed successfully.'
