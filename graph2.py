import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as plticker
from res import res


for stat in sorted(res.keys()):
	xs 		= [1, 2, 3, 4, 5]
	ys 		= [1490.8, 1202.0, 1132.8, 1041.0, 1104.0]
	
	ys 		= [1162.2, 1105.6, 919.6, 907.0, 1036.8]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	# plt.xscale("log", basex=2)
	plt.ylim(0, max(ys))
	plt.plot(xs, ys)
	ax.set_xticklabels(["", "Defaults", "#1", "#2", "#3", "#4"])
	ax.set_xlabel("Iteration")
	loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
	ax.xaxis.set_major_locator(loc)
	ax.set_ylabel("AverageLatency(us)")
	ax.set_title("Workload A Optimizer (50 Read/50 Write)")
	ax.set_title("Workload B Optimizer (95 Read/5 Write)")
	plt.savefig("graph_iter_2.png")