#!/usr/bin/env python

# python pi_mpi.py
# last edit April 23

# mpirun -np 5 python pi_mpi_gather.py

import time

def f(x):
    return 4.0/(1.0+x*x)

def trap(local_a,local_b,local_n,h):
    estimate = (f(local_a)+f(local_b))/2.0
    for i in xrange(1,local_n):
        x = local_a+float(i)*h
        estimate += f(x)
    #
    estimate *= h
    return estimate


from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank ==0:start = time.time()

b = 1.0
a = 0.0
n = 100000000
h = (b-a)/float(n)

local_n = int(n/size)
local_a = a+rank*float(local_n)*h
local_b = local_a+float(local_n)*h


local_int = trap(local_a,local_b,local_n,h)

comm.Barrier()
local_int = comm.gather(local_int, root=0)
if rank == 0:
	end = time.time()
	print "Pi with %d steps is %f in %f secs" %(n, sum(local_int), end-start)
