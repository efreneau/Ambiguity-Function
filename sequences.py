import numpy as np
import math

def zadoff_chu(u,N,q=0):
    cf = N%2
    n = np.linspace(0,N-1,N);
    
    return np.exp(-1j*math.pi*u*np.multiply(n,n+cf+2*q)/N)

def barker_13(up_sample_factor):
    b13 = np.array([1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1])
    return b13.repeat(up_sample_factor, axis=0)

def weierstrass(M, N):
    x = np.linspace(-1,1,M)
    M = np.size(x)
    y = np.zeros((N,M))
    for n in range(1,N):
        y[n,:] = np.cos((3**n)*np.pi*x)/2**n
    return x,np.sum(y,axis=0)

def MLFSR(seed):
    N = len(seed)
    
    register = seed
    output = np.zeros(int(2**N-1),dtype=np.bool)
    
    for i in range(0,2**N-2):
        carry = register[-1]     
        register = np.roll(register,1)
        register[0] = carry^register[-1]
        output[i] = carry
    return output.astype(float)
