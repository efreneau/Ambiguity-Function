#Computes a complex ambiguity function for a pulse. Returns a 2D array where the first axis time and the second is frequency.
#
#	waveform : array_like
#		The sequence of interest. A 1D array.
#
#	M_frequency_points : int,
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
	ambiguity = np.zeros((N,M_frequency_points),dtype=np.complex_);
	
	#Change approach based if the input waveform is complex
	
	if(M_frequency_points<N/2):
		warn("M_frequency_points < size(waveform)/2")
	
	#Generate roots of unity.
	
	#Generate shifted versions of the sequence.
	S_deck = deque(waveform);
	#S_1 = S_deck.rotate(1)  
	
	#Compute sum

	return ambiguity
