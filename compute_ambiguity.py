import warnings
import math
import numpy as np
from collections import deque


#Computes the ambiguity function for a sequence.
#The delay and doppler axis have as many increments as the input waveform. Output is (N,N)
#This code utilizes np.ifft to perform part of the calculation.

def ambiguity_function(waveform,circular_ambiguity=True,normalize=True):
	N = np.size(waveform)
	odd = False
	
	#If N is odd pad to make a more composite number
	if(N%2==1):
		S_0 = np.append(waveform,0).astype(complex)
		N = N+1
		odd = True
	else:
		S_0 = waveform.astype(complex) #ensure waveform is complex
	
	S_0 = S_0.reshape(N,)
	
	ambiguity = np.zeros((N,N),dtype=np.complex_)
	
	#create conjugate sequence
	S_conj = np.conj(S_0)
	
	#Generate shifted versions of the sequence, different complex sinusoids then do the multiplication and sum.
	for K in range(0,N):#Time shift
		if circular_ambiguity:
			Rxx_k = np.multiply(S_0,np.roll(S_conj,K)); #shift and element-wise multiply
		else:
			Rxx_k = np.multiply(S_0,right_shift(S_conj,K));	
			
		#for L in range(0,N):#Frequency shift
		ambiguity[K,:] = np.fft.fftshift(np.fft.ifft(Rxx_k))
	
	#ambiguity shift workaround
	ambiguity1 = np.zeros((N,N),dtype=np.complex_);
	
	ambiguity1[0:math.floor(N/2),:] = ambiguity[math.ceil(N/2):N,:];
	ambiguity1[math.ceil(N/2):N,:] = ambiguity[0:math.floor(N/2),:];
	
	ambiguity = np.swapaxes(ambiguity1,0,1)#flip axis
	
	if(normalize):
		ambiguity = ambiguity/np.amax(ambiguity)
	
	#Correct for padding
	if odd:
		return ambiguity[1:,1:]
	else:
		return ambiguity

#Computes a complex ambiguity function for a pulse. Returns a 2D array where the first axis is time delay and the second is doppler frequency.
#
#	waveform : array_like
#		The sequence of interest. A 1D array.
#
#	N : int
#		Controls the resolution of the time delay axis.
#		There are N increments in the delay axis.
#
#	M : int
#		Controls the spectral resolution of the doppler axis.
#
#	fs: double
#		Sample rate of the input signal.
#
#	circular_ambiguity : bool, optional
#		true(default): pulse treated as being transmitted back to back with another copy of the same pulse.
#		false: pulse treated as being transmitted in isolation (surrounded by zeros).
#
#Returns a complex (N,M) array

def ambiguity_function2(waveform,N,M,fs,circular_ambiguity=True,normalize=True): 
	fs = np.floor(fs)
	S_0 = waveform.astype(complex) #ensure waveform is complex
	sample_num = np.size(waveform)
		
	ambiguity = np.zeros((N,M),dtype=np.complex_)
	
	#create conjugate sequence
	S_conj = np.conj(S_0)
	
	t = np.linspace(0,sample_num/fs,sample_num)
	
	for i in range(0,N-1):
		#tau = K/fs
		K = int(i*sample_num/(N-1))
		
		if circular_ambiguity:#time delay
			Rxx_k = np.multiply(S_0,np.roll(S_conj,K)); #shift and element-wise multiply
		else:
			Rxx_k = np.multiply(S_0,right_shift(S_conj,K));		
		
		for L in range(0,M-1):#doppler shift
			f = -fs/2+L*fs/(M-1)#convert to continuous frequency
			kernel = np.exp(2j*math.pi*f*t)#Create frequency shift kernel
			ambiguity[K,L] = np.vdot(Rxx_k,kernel)/fs #integrate over time basis
				
	#ambiguity shift

	ambiguity1 = np.zeros((N,M),dtype=np.complex_);
	
	ambiguity1[0:int(N/2)-1,:] = ambiguity[int(N/2):N-1,:];
	ambiguity1[int(N/2):N-1,:] = ambiguity[0:int(N/2)-1,:];
	
	ambiguity = np.swapaxes(ambiguity1,0,1)#flip axis
	
	if(normalize):
		ambiguity = ambiguity/np.amax(ambiguity)

	return ambiguity

#Shift with no roll
def right_shift(sequence,shift):
	s = np.roll(sequence,shift)	#roll
	s[:shift] = 0				#set circularly shifted values to 0
	return s
