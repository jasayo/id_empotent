# fast factor calculation, found online
from math import sqrt
import functools
import itertools
import math
import numbthy # you'll need to find and download this separately
import sys
import time
import winsound

def beep():
    winsound.Beep(440,125)

def prompt():
        input("waiting...")
    
def isIdempotent(p_bar,q_bar):
    if (p_bar-1)*(q_bar-1) % numbthy.carmichael_lambda(p_bar*q_bar) == 0:
        return True
    return False

# Acts as if vec is numbered from 1.  Normally idx and vec are sets.
def gather(idx, vec):
        idx = list(idx)
        vec = list(vec)
        ans = []
        for i in idx:
                ans.append(vec[i-1])
        return ans

# turns factor lists like 324 = [(2,2),(3,4)] into [2,2,3,3,3,3]
def unravel(L):
    ans = []
    for (p,e) in L:
        for i in range(1,e+1):
           ans.append(p)
    return ans

# returns all nontrivial multiplicative partitions (p,q) such that n=pq and
# lambda(n) divides (p-1)(q-1).  One of (p,q) will be greater than 1.
def idempotentPartitions(n,factor_list):
    partitions_of_n = partitions(n,factor_list)
    ans = []
    for (p,q) in partitions_of_n:
        pseudo = (p-1)*(q-1)
        lambda_n = carmichael_lambda_with_list(n,factor_list)
        if pseudo % lambda_n == 0:
            ans.append((p,q))
    return ans

# returns True if all partitions of n are idempotent
def isMaximallyIdempotent(n):
    factor_list = numbthy.factor(n)
    ipList = idempotentPartitions(n, factor_list)
    numFactors = len(factor_list)
    if len(ipList) == 2**(numFactors-1)-1:
        return True
    return False

# returns all 2-factor idempotent multiplicative partitions of n
# where both components are composite
# assumes n square-free
def fullyCompositeIdempotentPartitions(n,factor_list):
    partitions_of_n = partitions(n,factor_list)
    ans = []
    for (p,q) in partitions_of_n:
        if numbthy.is_prime(p):
            continue
        if numbthy.is_prime(q):
            continue
        pseudo = (p-1)*(q-1)
        lambda_n = carmichael_lambda_with_list(n,factor_list)
        if pseudo % lambda_n == 0:
            ans.append((p,q))
    return ans

# returns all 2-factor idempotent multiplicative partitions of n
# where one component is prime and one is composite
# assumes n square-free
def semiCompositeIdempotentPartitions(n,factor_list):
    partitions_of_n = partitions(n,factor_list)
    ans = []
    for (p,q) in partitions_of_n:
        pIsPrime = numbthy.is_prime(p)
        qIsPrime = numbthy.is_prime(q)
        if pIsPrime and qIsPrime or (not pIsPrime and not qIsPrime):
            continue
        pseudo = (p-1)*(q-1)
        lambda_n = carmichael_lambda_with_list(n,factor_list)
        if pseudo % lambda_n == 0:
            ans.append((p,q))
    return ans


# returns all non-trivial 2-factor multiplicative partitions of n
# assumes n square-free
def partitions(n,factor_list):
    u_factor_list = unravel(factor_list)
    ans = []
    num_factors = len(factor_list)
    limit = (num_factors)//2
    L = range(1,num_factors+1)  # +1 because L needs to include num_factors
    even_nf = False
    if num_factors % 2 == 0:
        even_nf = True
    lambda_n = carmichael_lambda_with_list(n,factor_list)
    for i in range(1,limit+1):
        comb_list = list(itertools.combinations(L,i))
        if even_nf and i == limit:
            half = len(comb_list)//2
            comb_list = comb_list[:half]
        for c in comb_list:
            idx1 = set(c)
            idx2 = set(L)-set(c)
            list1 = gather(idx1,u_factor_list)
            list2 = gather(idx2,u_factor_list)
            factor1 = 1
            for p in list1:
                factor1 = factor1*p
            factor2 = 1
            for p in list2:
                factor2 = factor2*p                                
            ans.append((factor1, factor2))
    return list(set(ans))

# copied and tweaked from numbthy.py
def carmichael_lambda_with_list(n,factors):
	"""carmichael_lambda(n) - Compute Carmichael's Lambda function
	of n - the smallest exponent e such that b**e = 1 for all b coprime to n.
	Otherwise defined as the exponent of the group of integers mod n."""
	# SAGE equivalent is sage.crypto.util.carmichael_lambda(n)
	if n == 1: return 1
	if n <= 0: raise ValueError("*** Error ***:  Input n for carmichael_lambda(n) must be a positive integer.")
	# The gcd of (p**(e-1))*(p-1) for each prime factor p with multiplicity e (exception is p=2).
	def _carmichael_lambda_primepow(theprime,thepow):
		if ((theprime == 2) and (thepow >= 3)):
			return (2**(thepow-2)) # Z_(2**e) is not cyclic for e>=3
		else:
			return (theprime-1)*(theprime**(thepow-1))
	return functools.reduce(lambda accum,x:(accum*x)//numbthy.gcd(accum,x),tuple(_carmichael_lambda_primepow(*primepow) for primepow in factors),1)

def is_composite_and_square_free(n):
    for p in [2,3,5,7,11,13]:
        if n % p**2 == 0:
            return False
    factor_list = numbthy.factor(n) 
    if len(factor_list) == 1:
        return False;
    for (p,e) in factor_list:
        if (e > 1):
            return False
    return True

def is_square_free(n):
    for p in [2,3,5,7,11,13]:
        if n % p**2 == 0:
            return False
    factor_list = numbthy.factor(n) 
    for (p,e) in factor_list:
        if (e > 1):
            return False
    return True

def is_square_free_with_list(n,factor_list):
    for (p,e) in factor_list:
        if (e > 1):
            return False
    return True

def is_composite_and_square_free_with_list(n,factor_list):
    if len(factor_list) == 1:
        return False
    for (p,e) in factor_list:
        if (e > 1):
            return False
    return True

