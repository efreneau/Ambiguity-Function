#Computes a complex ambiguity function for a pulse. Returns a 2D array where the first axis time and the second is frequency.
#
#	waveform : array_like
#		The sequence of interest. A 1D array.
#
#	M : int
#		Controls the spectral resolution of the plot.
#		Negative frequency shifts and unshifted are also computed. 2*M+1 in total.
#
#	circular_ambiguity : bool, optional
#		true(default): pulse treated as being transmitted back to back with another copy of the same pulse.
#		false: pulse treated as being transmitted in isolation (surrounded by zeros).
#
#Returns a complex (N,2*M+1) array

import warnings
import math
import numpy as np
from collections import deque

def ambiguity_function(waveform,M,circular_ambiguity=True):
	N = np.size(waveform)
	S_0 = waveform.astype(complex) #ensure waveform is complex
	S_0 = S_0.reshape(N,)
	ambiguity = np.zeros((N,2*M+1),dtype=np.complex_)
	
	#Generate roots of unity to form a complex sinusoid.
	exponent = np.linspace(0,2*math.pi,N) #N points 0-2*pi (sequence is N long, so N shifts), divided by M to normalize the frequency axis
	W_N = np.exp(1j*exponent)
	
	#create conjugate sequence
	S_conj = np.conj(S_0)
	
	#Generate shifted versions of the sequence, different complex sinusoids then do the multiplication and sum.
	for K in range(0,N):#Time shift
		if circular_ambiguity:
			Rxx_k = np.multiply(S_0,np.roll(S_conj,K)); #shift and element-wise multiply
		else:
			Rxx_k = np.multiply(S_0,right_shift(S_conj,K));	
			
		for L in range(0,M):#Frequency shift
			if(L == 0):
				ambiguity[K,M] = np.sum(Rxx_k)									#No frequency shift, L=0 slice is the autocorrelation of S_0
			else:
				ambiguity[K,M-L] = np.vdot(np.power(W_N,-L),Rxx_k)				#negative frequency shift
				ambiguity[K,M+L] = np.vdot(np.power(W_N,L),Rxx_k)				#positive frequency shift
	
	return ambiguity

#Shift with no roll
def right_shift(sequence,shift):
	s = np.roll(sequence,shift)	#roll
	s[:shift] = 0				#set circularly shifted values to 0
	return s
