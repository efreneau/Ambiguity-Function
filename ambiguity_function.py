#Computes a complex ambiguity function for a pulse. Returns a 2D array where the first axis time and the second is frequency.
#
#	waveform : array_like
#		The sequence of interest. A 1D array.
#
#	M_frequency_points : int
#		Controls the spectral resolution of the plot.
#		Negative frequency components also computed. 2*M in positive and negative frequency points.
#		Useful values are <size(waveform)/2  
#
#	circular_ambiguity : bool, optional
#		true(default): pulse treated as being transmitted back to back with another copy of the same pulse.
#		false: pulse treated as being transmitted in isolation (surrounded by zeros).

import warnings
import numpy as np
from collections import deque

def ambiguity_function(waveform,M_frequency_points,circular_ambiguity=true):
	N = size(waveform);
	S_0 = waveform.astype(complex); #ensure waveform is complex
	ambiguity = np.zeros((N,2*M_frequency_points),dtype=np.complex_);
	
	if(M_frequency_points<N/2):
		warn("M_frequency_points < size(waveform)/2")
	
	#Generate roots of unity.
	exponent = linspace(0,2*pi/M_frequency_points,N,dtype=np.complex32);
	W_N = np.exp(exponent);
	
	#create conjugate sequence
	S_conj = np.conj(S_0);
	
	#Generate shifted versions of the sequence, different complex sinusoids then do the multiplication and sum.
	for L in range(0,M_frequency_points):
		for K in range(0,N):
			if(L == 0):
				ambiguity_function(K,0) = np.dot(S_0,S_deck.rotate(K));
			else:
				if circular_ambiguity:
					S_shift = np.roll(S_conj,K);
				else:
					S_shift = right_shift(S_conj,K);
				
				ambiguity_function(K,L) = np.dot(np.multiply(W_N**L,S_shift),S_0);							#negative frequency content
				ambiguity_function(K,M_frequency_points+L-1) = np.dot(np.multiply(W_N**-L,S_shift),S_0);	#positive frequency content
	
	return ambiguity

#Shift with no roll
def right_shift(sequence,shift):
	s = np.roll(sequence,shift);#roll
	s[:shift] = 0;#set circularly shifted values to 0
	return s
