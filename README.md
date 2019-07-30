## Peakdetect
[![PyPI](https://badge.fury.io/py/peakdetect.svg)](https://pypi.org/project/peakdetect)
[![Build](https://travis-ci.org/Anaxilaus/peakdetect.svg?branch=master)](https://travis-ci.org/Anaxilaus/peakdetect)
[![Python Version](https://img.shields.io/badge/python-2%20and%203-blue.svg)](./.travis.yml)

Simple peak detection library for Python based on [Billauer's work](http://billauer.co.il/peakdet.html) and [this gist](https://gist.github.com/sixtenbe/1178136). If you can improve this project, feel free to contribute.


## Installation
**Pip:**
```
$ pip install peakdetect
```

**Clone repository:**
```
$ git clone https://github.com/Anaxilaus/peakdetect
$ python peakdetect/setup.py install
```
*Requirements:* numpy, scipy and matplotlib. Setup installs requirements itself.


## Usage
**Example usage:**
```python
>>> import peakdetect
>>> peaks = peakdetect.peakdetect(y_axis, x_axis, lookahead, delta)
```

**Documentation on peakdetect function, keyword arguments:**
```
y_axis -- A list containing the signal over which to find peaks
    
x_axis -- A x-axis whose values correspond to the y_axis list and is used
    in the return to specify the position of the peaks. If omitted an
    index of the y_axis is used.
    (default: None)
    
lookahead -- distance to look ahead from a peak candidate to determine if
    it is the actual peak
    (default: 200) 
    '(samples / period) / f' where '4 >= f >= 1.25' might be a good value
    
delta -- this specifies a minimum difference between a peak and
    the following points, before a peak may be considered a peak. Useful
    to hinder the function from picking up false peaks towards to end of
    the signal. To work well delta should be set to delta >= RMSnoise * 5.
    (default: 0)
    When omitted delta function causes a 20% decrease in speed.
    When used Correctly it can double the speed of the function
```
