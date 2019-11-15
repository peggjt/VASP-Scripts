'''
The script extracts the final magnetic moments from the OUTCAR file
and prints them to a file named MagneticData.

The magnetic moments share the same order as the ions.
To use this script:

    python readMagnetism.py

The OUTCAR file must be present in the same dictionary.

The respective columns in the MagneticData file give 
the magnetic moments in the x, y, and z dimensions.

Author: James T. Pegg

'''

import os
from math import sqrt

xData = []
yData = []
zData = []

with open('OUTCAR', 'r+') as f:
    for n, line in enumerate(f):
        if ' magnetization (x)' in line:
            xmTitle = n
            xmStart = n + 4
        if ' magnetization (y)' in line:
            ymTitle = n
            ymStart = n + 4
        if ' magnetization (z)' in line:
            zmTitle = n
            zmStart = n + 4

with open('OUTCAR', 'r+') as f:
    for n, line in enumerate(f):
        if ('---' in line) and (n >= xmStart) and (n < ymTitle):
            xmEnd = n - 1
        if ('---' in line) and (n >= ymStart) and (n < zmTitle):
            ymEnd = n - 1
        if ('---' in line) and (n >= zmStart):
            zmEnd = n - 1

with open('OUTCAR', 'r+') as f:
    for n, line in enumerate(f):
        if (n >= xmStart) and (n <= xmEnd):
            xData.append(line.split()[5])
        if (n >= ymStart) and (n <= ymEnd):
            yData.append(line.split()[5])
        if (n >= zmStart) and (n <= zmEnd):
            zData.append(line.split()[5])

with open('MagneticData', 'a+') as f:
    f.write('{}\n'.format('Magnetic Data'))
    f.write('{}\n'.format('%s %15s %15s %15s'% ('x-axis', 'y-axis', 'z-axis', 'Total')))
    f.write('{}\n'.format('%s %15s %15s %15s'% ('----------', '----------', '----------', '----------')))
    for i in range(0, len(xData)):
        total = round(sqrt(float(xData[i])**2 + float(yData[i])**2 + float(zData[i])**2), 3)
        f.write('{}\n'.format('%s %15s %15s %15s'% (xData[i], yData[i], zData[i], total)))
