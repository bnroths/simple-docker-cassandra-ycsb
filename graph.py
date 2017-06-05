import matplotlib.pyplot as plt
import numpy as np

from res import res


for stat in sorted(res.keys()):
	xs 		= []
	ys 		= []
	ys_err 	= []
	for read_val in sorted(res[stat].keys()):
		ys.append(np.mean(res[stat][read_val]))
		ys_err.append(np.std(res[stat][read_val]))
		xs.append(read_val)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.xscale("log", basex=2)
	plt.ylim(0, max(ys))
	plt.errorbar(xs, ys, yerr=ys_err)
	ax.set_xlabel("# Concurrent Reads")
	ax.set_ylabel(stat)
	
	plt.savefig("graph_%s.png" % stat)