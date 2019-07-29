#!/usr/bin/python2


# Copyright (C) 2016 Sixten Bergman
# License WTFPL
#
# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. 
# You can redistribute it and/or modify it under the terms of the Do What The
# Fuck You Want To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.
#

import numpy as np
from math import pi, sqrt

__all__ = [
        'ACV_A1',
        'ACV_A2',
        'ACV_A3',
        'ACV_A4',
        'ACV_A5',
        'ACV_A6',
        'ACV_A7',
        'ACV_A8'
        ]



#Heavyside step function
H_num = lambda t: 1 if t > 0 else 0
H = lambda T: np.asarray([1 if t > 0 else 0 for t in T])

# pure sine
def ACV_A1(T, Hz=50):
    """
    Generate a pure sine wave at a specified frequency
    
    keyword arguments:
    T -- time points to generate the waveform given in seconds
    Hz -- The desired frequency of the signal (default:50)
    """
    ampl = 1000
    T = np.asarray(T, dtype=np.float64)
    return ampl * sqrt(2) * np.sin(2*pi*Hz * T)

    
def ACV_A2(T, Hz=50):
    """
    Generate a pure sine wave with a DC offset at a specified frequency
    
    keyword arguments:
    T -- time points to generate the waveform given in seconds
    Hz -- The desired frequency of the signal (default:50)
    """
    ampl = 1000
    offset = 500
    T = np.asarray(T, dtype=np.float64)
    return ampl * sqrt(2) * np.sin(2*pi*Hz * T) + offset

    
def ACV_A3(T, Hz=50):
    """
    Generate a fundamental with a 3rd overtone
    
    keyword arguments:
    T -- time points to generate the waveform given in seconds
    Hz -- The desired frequency of the signal (default:50)
    """
    ampl = 1000
    T = np.asarray(T, dtype=np.float64)
    main_wave = np.sin(2*pi*Hz * T)
    harmonic_wave = 0.05 * np.sin(2*pi*Hz * T * 4 + pi * 2 / 3)
    return ampl * sqrt(2) * (main_wave + harmonic_wave)

    
def ACV_A4(T, Hz=50):
    """
    Generate a fundamental with a 4th overtone
    
    keyword arguments:
    T -- time points to generate the waveform given in seconds
    Hz -- The desired frequency of the signal (default:50)
    """
    ampl = 1000
    T = np.asarray(T, dtype=np.float64)
    main_wave = np.sin(2*pi*Hz * T)
    harmonic_wave = 0.07 * np.sin(2*pi*Hz * T * 5 + pi * 22 / 18)
    return ampl * sqrt(2) * (main_wave + harmonic_wave)
    
    
def ACV_A5(T, Hz=50):
    """
    Generate a realistic triangle wave
    
    keyword arguments:
    T -- time points to generate the waveform given in seconds
    Hz -- The desired frequency of the signal (default:50)
    """
    ampl = 1000
    T = np.asarray(T, dtype=np.float64)
    wave_1 = np.sin(2*pi*Hz * T)
    wave_2 = 0.05 * np.sin(2*pi*Hz * T * 3 - pi)
    wave_3 = 0.05 * np.sin(2*pi*Hz * T * 5)
    wave_4 = 0.02 * np.sin(2*pi*Hz * T * 7 - pi)
    wave_5 = 0.01 * np.sin(2*pi*Hz * T * 9)
    return ampl * sqrt(2) * (wave_1 + wave_2 + wave_3 + wave_4 + wave_5)
    
    
def ACV_A6(T, Hz=50):
    """
    Generate a realistic triangle wave
    
    keyword arguments:
    T -- time points to generate the waveform given in seconds
    Hz -- The desired frequency of the signal (default:50)
    """
    ampl = 1000
    T = np.asarray(T, dtype=np.float64)
    wave_1 = np.sin(2*pi*Hz * T)
    wave_2 = 0.02 * np.sin(2*pi*Hz * T * 3 - pi)
    wave_3 = 0.02 * np.sin(2*pi*Hz * T * 5)
    wave_4 = 0.0015 * np.sin(2*pi*Hz * T * 7 - pi)
    wave_5 = 0.009 * np.sin(2*pi*Hz * T * 9)
    return ampl * sqrt(2) * (wave_1 + wave_2 + wave_3 + wave_4 + wave_5)
    
    
def ACV_A7(T, Hz=50):
    """
    Generate a growing sine wave, where the wave starts at 0 and reaches 0.9 of
    full amplitude at 250 cycles. Thereafter it will linearly increase to full
    amplitude at 500 cycles and terminate to 0
    
    Frequency locked to 50Hz and = 0 at t>10
    
    keyword arguments:
    T -- time points to generate the waveform given in seconds
    Hz -- The desired frequency of the signal (default:50)
    """
    ampl = 1000
    Hz = 50
    T = np.asarray(T, dtype=np.float64)
    wave_main = np.sin(2*pi*Hz * T)
    step_func = (0.9 * T / 5 * H(5-T) + H(T-5) * H(10-T) * (0.9 + 0.1 * (T-5) / 5))
    return ampl * sqrt(2) * wave_main * step_func
    
def ACV_A8(T, Hz=50):
    """
    Generate a growing sine wave, which reaches 100 times the amplitude at
    500 cycles
    
    frequency not implemented and signal = 0 at t>1000*pi
    signal frequency = 0.15915494309189535 Hz?
    
    keyword arguments:
    T -- time points to generate the waveform given in seconds
    Hz -- The desired frequency of the signal (default:50)
    """
    ampl = 1000
    Hz = 50
    T = np.asarray(T, dtype=np.float64)
    wave_main = np.sin(T)
    step_func = T / (10 * pi) * H(10 - T / (2*pi*Hz))
    return ampl * sqrt(2) * wave_main * step_func
    
 
_ACV_A1_L = lambda T, Hz = 50: 1000 * sqrt(2) * np.sin(2*pi*Hz * T)
# 
_ACV_A2_L = lambda T, Hz = 50: 1000 * sqrt(2) * np.sin(2*pi*Hz * T) + 500
# 
_ACV_A3_L = lambda T, Hz = 50: 1000 * sqrt(2) * (np.sin(2*pi*Hz * T) + 
                            0.05 * np.sin(2*pi*Hz * T * 4 + pi * 2 / 3))
#     
_ACV_A4_L = lambda T, Hz = 50:( 1000 * sqrt(2) * (np.sin(2*pi*Hz * T) + 
                            0.07 * np.sin(2*pi*Hz * T * 5 + pi * 22 / 18)))

# Realistic triangle
_ACV_A5_L = lambda T, Hz = 50:( 1000 * sqrt(2) * (np.sin(2*pi*Hz * T) + 
                            0.05 * np.sin(2*pi*Hz * T * 3 - pi) + 
                            0.05 * np.sin(2*pi*Hz * T * 5) + 
                            0.02 * np.sin(2*pi*Hz * T * 7 - pi) +
                            0.01 * np.sin(2*pi*Hz * T * 9)))
# 
_ACV_A6_L = lambda T, Hz = 50:( 1000 * sqrt(2) * (np.sin(2*pi*Hz * T) + 
                            0.02 * np.sin(2*pi*Hz * T * 3 - pi) + 
                            0.02 * np.sin(2*pi*Hz * T * 5) + 
                            0.0015 * np.sin(2*pi*Hz * T * 7 - pi) + 
                            0.009 * np.sin(2*pi*Hz * T * 9)))

#A7 & A8 convert so that a input of 16*pi corresponds to a input 0.25 in the current version
_ACV_A7_OLD = lambda T: [1000 * sqrt(2) * np.sin(100 * pi * t) *
        (0.9 * t / 5 * H_num(5-t) + H_num(t-5) * H_num(10-t) * (0.9 + 0.1 * (t-5) / 5)) for t in T]
_ACV_A8_OLD = lambda T: [1000 * sqrt(2) * np.sin(t) * 
        t / (10 * pi) * H_num(10 - t / (100 * pi)) for t in T]



if __name__ == "__main__":
    #create 1 period triangle
    x = np.linspace(0, 0.02, 4000)
    y = ACV_A5(x)
    
    