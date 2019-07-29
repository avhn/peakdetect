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

import analytic_wfm
import numpy as np
import peakdetect
import unittest
import pdb

#generate time axis for 5 cycles @ 50 Hz
linspace_standard = np.linspace(0, 0.10, 1000)
linspace_peakdetect = np.linspace(0, 0.10, 10000)

def prng():
    """
    A numpy random number generator with a known starting state
    
    return: a random number generator
    """
    return np.random.RandomState(773889874)


def _write_log(file, header, message):
    with open(file, "ab") as f:
        f.write(header)
        f.write("\n")
        f.writelines(message)
        f.write("\n")
        f.write("\n")
        
        
def _calculate_missmatch(received, expected):
    """
    Calculates the mean mismatch between received and expected data
    
    keyword arguments:
    received -- [[time of peak], [ampl of peak]]
    expected -- [[time of peak], [ampl of peak]]
    
    return (time mismatch, ampl mismatch)
    """
    #t_diff = np.abs(np.asarray(received[0]) - expected[0])
    t_diff = np.asarray(received[0]) - expected[0]
    a_diff = np.abs(np.asarray(received[1]) - expected[1])
    
    
    #t_diff /= np.abs(expected[0]) time error in absolute terms
    a_diff /= np.abs(expected[1])
    
    return (t_diff, a_diff)
    
    
def _log_diff(t_max, y_max, 
            t_min, y_min,
            t_max_expected, y_max_expected,
            t_min_expected, y_min_expected,
            file, name
            ):
    """
    keyword arguments:
    t_max -- time of maxima
    y_max -- amplitude of maxima
    t_min -- time of minima
    y_min -- amplitude of maxima
    t_max_expected -- expected time of maxima
    y_max_expected -- expected amplitude of maxima
    t_min_expected -- expected time of minima
    y_min_expected -- expected amplitude of maxima
    file -- log file to write to
    name -- name of the test performed
    """
    t_diff_h, a_diff_h = _calculate_missmatch([t_max, y_max],
            [t_max_expected, y_max_expected])
    
    
    t_diff_l, a_diff_l = _calculate_missmatch([t_min, y_min],
            [t_min_expected, y_min_expected])
            
    #data = ["\t{0:.2e}\t{1:.2e}\t{2:.2e}\t{3:.2e}".format(*d) for d in 
    #        [t_diff_h, t_diff_l, a_diff_h, a_diff_l]
    #    ]
    frt = "val:{0} error:{1:.2e}"
    data = ["\t{0}".format("\t".join(map(frt.format, val, err))) for val, err in
        [(t_max, t_diff_h), 
        (t_min, t_diff_l), 
        (y_max, a_diff_h), 
        (y_min, a_diff_l)]
        ]
    
    _write_log(file, name, "\n".join(data))
    
    
    
def _is_close(max_p, min_p, 
        expected_max, expected_min, 
        atol_time, tol_ampl,
        file, name):
    """
    Determines if the peaks are within the given tolerance
    
    keyword arguments:
    max_p -- location and value of maxima
    min_p -- location and value of minima
    expected_max -- expected location and value of maxima
    expected_min -- expected location and value of minima
    atol_time -- absolute tolerance of location of vertex
    tol_ampl -- relative tolerance of value of vertex
    file -- log file to write to
    name -- name of the test performed
    """
    if len(max_p) == 5:
        t_max_expected, y_max_expected = zip(*expected_max)
    else:
        if abs(max_p[0][0] - expected_max[0][0]) > 0.001:
            t_max_expected, y_max_expected = zip(*expected_max[1:])
        else:
            t_max_expected, y_max_expected = zip(*expected_max[:-1])
        
    if len(min_p) == 5:
        t_min_expected, y_min_expected = zip(*expected_min)
    else:
        t_min_expected, y_min_expected = zip(*expected_min[:-1])
    
    t_max, y_max = zip(*max_p)
    t_min, y_min = zip(*min_p)
    
    t_max_close = np.isclose(t_max, t_max_expected, atol=atol_time, rtol=1e-12)
    y_max_close = np.isclose(y_max, y_max_expected, tol_ampl)
    t_min_close = np.isclose(t_min, t_min_expected, atol=atol_time, rtol=1e-12)
    y_min_close = np.isclose(y_min, y_min_expected, tol_ampl)
    
    
    _log_diff(t_max, y_max, t_min, y_min, 
            t_max_expected, y_max_expected,
            t_min_expected, y_min_expected,
            file, name)

    return(t_max_close, y_max_close, t_min_close, y_min_close)




class Test_analytic_wfm(unittest.TestCase):
    def test_ACV1(self):
        #compare with previous lambda implementation
        old = analytic_wfm._ACV_A1_L(linspace_standard)
        acv = analytic_wfm.ACV_A1(linspace_standard)
        
        self.assertTrue(np.allclose(acv, old, rtol=1e-9))
        
    def test_ACV2(self):
        #compare with previous lambda implementation
        old = analytic_wfm._ACV_A2_L(linspace_standard)
        acv = analytic_wfm.ACV_A2(linspace_standard)
        
        self.assertTrue(np.allclose(acv, old, rtol=1e-9))
        
    def test_ACV3(self):
        #compare with previous lambda implementation
        old = analytic_wfm._ACV_A3_L(linspace_standard)
        acv = analytic_wfm.ACV_A3(linspace_standard)
        
        self.assertTrue(np.allclose(acv, old, rtol=1e-9))
        
    def test_ACV4(self):
        #compare with previous lambda implementation
        old = analytic_wfm._ACV_A4_L(linspace_standard)
        acv = analytic_wfm.ACV_A4(linspace_standard)
        
        self.assertTrue(np.allclose(acv, old, rtol=1e-9))
        
    def test_ACV5(self):
        #compare with previous lambda implementation
        old = analytic_wfm._ACV_A5_L(linspace_standard)
        acv = analytic_wfm.ACV_A5(linspace_standard)
        
        self.assertTrue(np.allclose(acv, old, rtol=1e-9))
        
    def test_ACV6(self):
        #compare with previous lambda implementation
        old = analytic_wfm._ACV_A6_L(linspace_standard)
        acv = analytic_wfm.ACV_A6(linspace_standard)
        
        self.assertTrue(np.allclose(acv, old, rtol=1e-9))
        
        
    def test_ACV7(self):
        num = np.linspace(0, 20, 1000)
        old = analytic_wfm._ACV_A7_OLD(num)
        acv = analytic_wfm.ACV_A7(num)
        
        self.assertTrue(np.allclose(acv, old, rtol=1e-9))
        
        
    def test_ACV8(self):
        num = np.linspace(0, 3150, 10000)
        old = analytic_wfm._ACV_A8_OLD(num)
        acv = analytic_wfm.ACV_A8(num)
        
        self.assertTrue(np.allclose(acv, old, rtol=1e-9))
        
        
        
        
class _Test_peakdetect_template(unittest.TestCase):
    func = None
    file = "Mismatch data.txt"
    name = "template"
    args = []
    kwargs = {}
    msg_t = "Time of {0!s} not within tolerance:\n\t{1}"
    msg_y = "Amplitude of {0!s} not within tolerance:\n\t{1}"
    
    def _test_peak_template(self, waveform, 
            expected_max, expected_min, 
            wav_name,
            atol_time = 1e-5, tol_ampl = 1e-5):
        """
        
        keyword arguments:
        waveform -- a function that given x can generate a test waveform
        expected_max -- position and amplitude where maxima are expected
        expected_min -- position and amplitude where minima are expected
        wav_name -- Name of the test waveform
        atol_time -- absolute tolerance for position of vertex (default: 1e-5)
        tol_ampl -- relative tolerance for position of vertex (default: 1e-5)
        """
        
        y = waveform(linspace_peakdetect)
        max_p, min_p = self.func(y, linspace_peakdetect, 
            *self.args, **self.kwargs
            )
        #check if the correct amount of peaks were discovered
        self.assertIn(len(max_p), [4,5])
        self.assertIn(len(min_p), [4,5])
        
        #
        # check if position and amplitude is within 0.001% which is approx the
        # numeric uncertainty from the amount of samples used
        #
        t_max_close, y_max_close, t_min_close, y_min_close = _is_close(max_p,
            min_p, 
            expected_max, 
            expected_min, 
            atol_time, tol_ampl,
            self.file, "{0}: {1}".format(wav_name, self.name))
        
        #assert if values are outside of tolerance
        self.assertTrue(np.all(t_max_close),
            msg=self.msg_t.format("maxima", t_max_close))
        self.assertTrue(np.all(y_max_close),
            msg=self.msg_y.format("maxima", y_max_close))
        
        self.assertTrue(np.all(t_min_close),
            msg=self.msg_t.format("minima", t_min_close))
        self.assertTrue(np.all(y_min_close),
            msg=self.msg_y.format("minima", y_min_close))
            
            
    def test_peak_ACV1(self):
        peak_pos = 1000*np.sqrt(2) #1414.2135623730951
        peak_neg = -peak_pos
        expected_max = [
                (0.005, peak_pos),
                (0.025, peak_pos),
                (0.045, peak_pos),
                (0.065, peak_pos),
                (0.085, peak_pos)
                ]
        expected_min = [
                (0.015, peak_neg),
                (0.035, peak_neg),
                (0.055, peak_neg),
                (0.075, peak_neg),
                (0.095, peak_neg)
                ]
        atol_time = 1e-5
        tol_ampl = 1e-6
        
        self._test_peak_template(analytic_wfm.ACV_A1,
            expected_max, expected_min,
            "ACV1",
            atol_time, tol_ampl
            )
            
    def test_peak_ACV2(self):
        peak_pos = 1000*np.sqrt(2) + 500 #1414.2135623730951 + 500
        peak_neg = (-1000*np.sqrt(2)) + 500 #-914.2135623730951
        expected_max = [
                (0.005, peak_pos),
                (0.025, peak_pos),
                (0.045, peak_pos),
                (0.065, peak_pos),
                (0.085, peak_pos)
                ]
        expected_min = [
                (0.015, peak_neg),
                (0.035, peak_neg),
                (0.055, peak_neg),
                (0.075, peak_neg),
                (0.095, peak_neg)
                ]
        atol_time = 1e-5
        tol_ampl = 2e-6
        
        self._test_peak_template(analytic_wfm.ACV_A2,
            expected_max, expected_min, 
            "ACV2",
            atol_time, tol_ampl
            )
    
    
    def test_peak_ACV3(self):
        """
        Sine wave with a 3rd overtone
        
        WolframAlpha solution
        
        max{y = sin(100 pi x)+0.05 sin(400 pi x+(2 pi)/3)}~~
        sin(6.28319 n+1.51306)-0.05 sin(25.1327 n+5.00505) 
        at x~~0.00481623+0.02 n for integer n
        
        min{y = sin(100 pi x)+0.05 sin(400 pi x+(2 pi)/3)}~~
        0.05 sin(6.55488-25.1327 n)-sin(1.37692-6.28319 n)
        at x~~-0.00438287+0.02 n for integer n
        
        Derivative for 50 Hz in 2 alternative forms
        y = 100pi*cos(100pi*x) - 25pi*cos(400pi*x)-0.3464*50*pi*sin(400pi*x)
        y = 100pi*cos(100pi*x) + 20pi*cos(400pi*x + 2*pi/3)
        
        root 0 = 1/(50 * pi) * (pi*0 - 0.68846026579266880983)
        The exact solution according to WolframAlpha - I haven't the foggiest
        (tan^(-1)(root of 
            {#1^2-3&, 11 #2^8-8 #1 #2^7-8 #2^6+56 #1 #2^5+70 #2^4-56 #1 #2^3-48 #2^2+8 #1 #2-9&}(x) 
            near x = -0.822751)+pi n) / (50 * pi)
            
            
        root 1 = 1/(50 * pi) * (pi*0 + 0.75653155241276430710)
        
        period = 0.02
        """
        base = 1000*np.sqrt(2)
        
        #def peak_pos(n):
        #    return base * (np.sin(6.28319 * n + 1.51306) 
        #        -0.05*np.sin(25.1327 * n + 5.00505))
        #def peak_neg(n):
        #    return base * (0.05 * np.sin(6.55488 - 25.1327 * n)
        #        - np.sin(1.37692 - 6.28319 * n))
        
        
        def peak_pos(n):
            return base * (np.sin(2*np.pi * n + 1.51306) 
                -0.05*np.sin(8*np.pi * n + 5.00505))
        def peak_neg(n):
            return base * (0.05 * np.sin(6.55488 - 8*np.pi * n)
                - np.sin(1.37692 - 2*np.pi * n))
        t_max = [
                0.75653155241276430710/(50*np.pi)+0.00,#0.004816229446859069
                0.75653155241276430710/(50*np.pi)+0.02,#0.024816229446859069
                0.75653155241276430710/(50*np.pi)+0.04,#0.044816229446859069
                0.75653155241276430710/(50*np.pi)+0.06,#0.064816229446859069
                0.75653155241276430710/(50*np.pi)+0.08 #0.084816229446859069
                ]
        t_min = [
                -0.68846026579266880983/(50*np.pi)+0.02,#0.015617125823069466
                -0.68846026579266880983/(50*np.pi)+0.04,#0.035617125823069466
                -0.68846026579266880983/(50*np.pi)+0.06,#0.055617125823069466
                -0.68846026579266880983/(50*np.pi)+0.08,#0.075617125823069466
                -0.68846026579266880983/(50*np.pi)+0.10 #0.095617125823069466
                ]        
        
        expected_max = [
                (t_max[0], analytic_wfm.ACV_A3(t_max[0])),
                (t_max[1], analytic_wfm.ACV_A3(t_max[1])),
                (t_max[2], analytic_wfm.ACV_A3(t_max[2])),
                (t_max[3], analytic_wfm.ACV_A3(t_max[3])),
                (t_max[4], analytic_wfm.ACV_A3(t_max[4])),
                ]
        expected_min = [
                (t_min[0], analytic_wfm.ACV_A3(t_min[0])),
                (t_min[1], analytic_wfm.ACV_A3(t_min[1])),
                (t_min[2], analytic_wfm.ACV_A3(t_min[2])),
                (t_min[3], analytic_wfm.ACV_A3(t_min[3])),
                (t_min[4], analytic_wfm.ACV_A3(t_min[4])),
                ]
        atol_time = 1e-5
        tol_ampl = 2e-6
        #reduced tolerance since the expected values are only approximated
        
        self._test_peak_template(analytic_wfm.ACV_A3,
            expected_max, expected_min,
            "ACV3",
            atol_time, tol_ampl
            )
            
    def test_peak_ACV4(self):
        """
        Sine wave with a 4th overtone
        
        Expected data is from a numerical solution using 1e8 samples
        The numerical solution used about 2 GB memory and required 64-bit
        python
        
        Test is currently disabled as it pushes time index forward enough to
        change what peaks are discovers by peakdetect_fft, such that the last
        maxima is lost instead of the first one, which is expected from all the
        other functions
        """
        expected_max = [
                (0.0059351920593519207, 1409.2119572886963),
                (0.025935191259351911, 1409.2119572887088),
                (0.045935191459351918, 1409.2119572887223),
                (0.065935191659351911, 1409.2119572887243),
                (0.085935191859351917, 1409.2119572887166)
                ]
        expected_min = [
                (0.015935191159351911, -1409.2119572886984),
                (0.035935191359351915, -1409.2119572887166),
                (0.055935191559351914, -1409.2119572887245),
                (0.075935191759351914, -1409.2119572887223),
                (0.09593519195935192, -1409.2119572887068)
                ]
        atol_time = 1e-5
        tol_ampl = 2.5e-6
        #reduced tolerance since the expected values are only approximated
        
        self._test_peak_template(analytic_wfm.ACV_A4,
            expected_max, expected_min,
            "ACV4",
            atol_time, tol_ampl
            )
     
     
    def test_peak_ACV5(self):
        """
        Realistic triangle wave
        
        Easy enough to solve, but here is the numerical solution from 1e8
        samples. Numerical solution used about 2 GB memory and required
        64-bit python
        
        expected_max = [
                [0.0050000000500000008, 1598.0613254815967]
                [0.025000000250000001, 1598.0613254815778],
                [0.045000000450000008, 1598.0613254815346],
                [0.064999999650000001, 1598.0613254815594],
                [0.084999999849999994, 1598.0613254815908]
                ]
        expected_min = [
                [0.015000000150000001, -1598.0613254815908],
                [0.035000000350000005, -1598.0613254815594],
                [0.054999999549999998, -1598.0613254815346],
                [0.074999999750000004, -1598.0613254815778],
                [0.094999999949999997, -1598.0613254815967]
                ]
        """
        peak_pos = 1130*np.sqrt(2)    #1598.0613254815976
        peak_neg = -1130*np.sqrt(2)   #-1598.0613254815967
        expected_max = [
                (0.005, peak_pos),
                (0.025, peak_pos),
                (0.045, peak_pos),
                (0.065, peak_pos),
                (0.085, peak_pos)
                ]
        expected_min = [
                (0.015, peak_neg),
                (0.035, peak_neg),
                (0.055, peak_neg),
                (0.075, peak_neg),
                (0.095, peak_neg)
                ]
        atol_time = 1e-5
        tol_ampl = 4e-6
        
        self._test_peak_template(analytic_wfm.ACV_A5,
            expected_max, expected_min,
            "ACV5",
            atol_time, tol_ampl
            )
     
     
    def test_peak_ACV6(self):
        """
        Realistic triangle wave
        
        Easy enough to solve, but here is the numerical solution from 1e8
        samples. Numerical solution used about 2 GB memory and required
        64-bit python
        
        expected_max = [
                [0.0050000000500000008, 1485.6313472729362],
                [0.025000000250000001, 1485.6313472729255],
                [0.045000000450000008, 1485.6313472729012],
                [0.064999999650000001, 1485.6313472729153],
                [0.084999999849999994, 1485.6313472729323]
                ]
        expected_min = [
                [0.015000000150000001, -1485.6313472729323],
                [0.035000000350000005, -1485.6313472729153],
                [0.054999999549999998, -1485.6313472729012],
                [0.074999999750000004, -1485.6313472729255],
                [0.094999999949999997, -1485.6313472729362]
                ]
        """
        peak_pos = 1050.5*np.sqrt(2)    #1485.6313472729364
        peak_neg = -1050.5*np.sqrt(2)   #1485.6313472729255
        expected_max = [
                (0.005, peak_pos),
                (0.025, peak_pos),
                (0.045, peak_pos),
                (0.065, peak_pos),
                (0.085, peak_pos)
                ]
        expected_min = [
                (0.015, peak_neg),
                (0.035, peak_neg),
                (0.055, peak_neg),
                (0.075, peak_neg),
                (0.095, peak_neg)
                ]
        atol_time = 1e-5
        tol_ampl = 2.5e-6
        
        self._test_peak_template(analytic_wfm.ACV_A6,
            expected_max, expected_min,
            "ACV6",
            atol_time, tol_ampl
            )
            
    
            
            
            
class Test_peakdetect(_Test_peakdetect_template):
    name = "peakdetect"
    def __init__(self, *args, **kwargs):
        super(Test_peakdetect, self).__init__(*args, **kwargs)
        self.func = peakdetect.peakdetect
 
 
class Test_peakdetect_fft(_Test_peakdetect_template):
    name = "peakdetect_fft"
    def __init__(self, *args, **kwargs):
        super(Test_peakdetect_fft, self).__init__(*args, **kwargs)
        self.func = peakdetect.peakdetect_fft
            
        
class Test_peakdetect_parabola(_Test_peakdetect_template):
    name = "peakdetect_parabola"
    def __init__(self, *args, **kwargs):
        super(Test_peakdetect_parabola, self).__init__(*args, **kwargs)
        self.func = peakdetect.peakdetect_parabola
            
        
class Test_peakdetect_sine(_Test_peakdetect_template):
    name = "peakdetect_sine"
    def __init__(self, *args, **kwargs):
        super(Test_peakdetect_sine, self).__init__(*args, **kwargs)
        self.func = peakdetect.peakdetect_sine
            
        
class Test_peakdetect_sine_locked(_Test_peakdetect_template):
    name = "peakdetect_sine_locked"
    def __init__(self, *args, **kwargs):
        super(Test_peakdetect_sine_locked, self).__init__(*args, **kwargs)
        self.func = peakdetect.peakdetect_sine_locked
            
        
class Test_peakdetect_spline(_Test_peakdetect_template):
    name = "peakdetect_spline"
    def __init__(self, *args, **kwargs):
        super(Test_peakdetect_spline, self).__init__(*args, **kwargs)
        self.func = peakdetect.peakdetect_spline
            
        
class Test_peakdetect_zero_crossing(_Test_peakdetect_template):
    name = "peakdetect_zero_crossing"
    def __init__(self, *args, **kwargs):
        super(Test_peakdetect_zero_crossing, self).__init__(*args, **kwargs)
        self.func = peakdetect.peakdetect_zero_crossing
        
        
        
        
class Test_peakdetect_misc(unittest.TestCase):
    def test__pad(self):
        data = [1,2,3,4,5,6,5,4,3,2,1]
        pad_len = 2
        pad = lambda x, c: x[:len(x) // 2] + [0] * c + x[len(x) // 2:]
        expected = pad(list(data), 2 ** 
                peakdetect._n(len(data) * pad_len) - len(data))
        received = peakdetect._pad(data, pad_len)
        
        self.assertListEqual(received, expected)
    def test__n(self):
        self.assertEqual(2**peakdetect._n(1000), 1024)
        
    def test_zero_crossings(self):
        y = analytic_wfm.ACV_A1(linspace_peakdetect)
        expected_indice = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        indice = peakdetect.zero_crossings(y, 50)
        msg = "index:{0:d} should be within 1 of expected:{1:d}"
        for rec, exp in zip(indice, expected_indice):
            self.assertAlmostEqual(rec, exp, delta=1, msg=msg.format(rec, exp))
        
    
        
            
        
#class zero_crossings(unittest.TestCase):
            
        
        
        
if __name__ == "__main__":
    tests_to_run = [
                #Test_analytic_wfm,
                Test_peakdetect,
                Test_peakdetect_parabola,
                Test_peakdetect_fft,
                #Test_peakdetect_sine,  #sine tests disabled pending rework
                #Test_peakdetect_sine_locked,
                Test_peakdetect_spline,
                Test_peakdetect_zero_crossing,
                Test_peakdetect_misc
                ]
    
    suites_list = [unittest.TestLoader().loadTestsFromTestCase(test_class) for test_class in tests_to_run]
    big_suite = unittest.TestSuite(suites_list)
    unittest.TextTestRunner(verbosity=2).run(big_suite)