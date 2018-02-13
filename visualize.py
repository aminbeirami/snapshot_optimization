import matplotlib.pyplot as pl
import numpy as np

def queries():
	query_list = []
	with open("data/queries.txt") as f:
		for line in f:
			query_list.append(line)
	f.close()
	return query_list

def overall(name):
	cost_list = []
	with open("data/"+name+"_cost.txt") as f:
		for lines in f:
			data = lines.split(",")
			cost_list.append(data)
	f.close()
	for i in range(len(cost_list)):
		cost_list[i][1] = (cost_list[i][1].rstrip())
	return cost_list

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

def dyn_vs_rec_query():
	rec_no = []
	time_cost_dyn = []
	time_cost_rec = []
	with open ("data/dynamic_multiquery.txt") as f:
		for line in f:
			fields = line.split(',')
			rec_no.append(fields[0])
			time_cost_dyn.append(fields[1])
	f.close()
	with open("data/recursive_multiquery.txt") as p:
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
	pl.savefig('graphs/multiquery_runtime.png', bbox_inches='tight')

def dyn_vs_rec_snap():
	rec_no = []
	time_cost_dyn = []
	time_cost_rec = []
	with open ("data/dynamic_multisnap.txt") as f:
		for line in f:
			fields = line.split(',')
			rec_no.append(fields[0])
			time_cost_dyn.append(fields[1])
	f.close()
	with open("data/recursive_multisnap.txt") as p:
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
	pl.savefig('graphs/multisnap_runtime.png', bbox_inches='tight')

def plot_overall_cost():
	cost_list = overall("overall")
	cost_list.reverse()
	x = np.arange(len(cost_list))
	names = [n[0] for n in cost_list]
	cost = [c[1] for c in cost_list]
	pl.figure(facecolor = 'white')
	pl.bar(x, cost, width = 0.2,align = 'center', color = 'gray')
	pl.xticks(x, names)
	pl.xlabel('slicing method')
	pl.ylabel('overall cost')
	pl.savefig("graphs/cuts_cost.png")

def plot_individual_cost():
	cost_list = overall("individual")
	x = np.arange(len(cost_list))
	names = [n[0] for n in cost_list]
	cost = [c[1] for c in cost_list]
	pl.figure(facecolor = 'white')
	pl.bar(x, cost, width = 0.2,align = 'center', color = 'gray')
	pl.xticks(x, names)
	pl.xlabel('numbre of snapshots')
	pl.ylabel('overall cost')
	pl.savefig("graphs/snap_cost.png")


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
dyn_vs_rec_query()
dyn_vs_rec_snap()
plot_overall_cost()
plot_individual_cost()
# plot_single_cost()
# plot_multiple_cost()
print 'visualization completed successfully.'
