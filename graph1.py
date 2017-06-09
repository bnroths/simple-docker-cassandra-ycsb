import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from res1 import res1


for stat in sorted(res1.keys()):
	xs 		= []
	zs 		= []
	ys 		= []
	ys_err 	= []
	for read_val in sorted(res1[stat].keys()):
		reads, writes = read_val.split("-")
		zs.append(np.mean(res1[stat][read_val]))
		xs.append(reads)
		ys.append(writes)
		zs = [int(x) for x in zs]
		xs = [int(x) for x in xs]
		ys = [int(x) for x in ys]

	print xs
	print ys
	print zs
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	# plt.xscale("log", basex=2)
	# plt.yscale("log", basex=2)

	ax.scatter(xs, ys, zs, c='r', marker='o')
	ax.set_xlabel("# Concurrent Reads")
	ax.set_ylabel("# Concurrent Write")
	ax.set_zlabel(stat)
	
	plt.savefig("graph1_%s.png" % stat)

	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# plt.xscale("log", basex=2)
	# plt.ylim(0, max(ys))
	# plt.errorbar(xs, ys, yerr=ys_err)
	# ax.set_xlabel("# Concurrent Reads")
	# ax.set_ylabel(stat)
	
	# plt.savefig("graph_%s.png" % stat)