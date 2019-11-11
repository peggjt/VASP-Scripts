import os

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
        for i in range(0, len(xData)):
                f.write('{}\n'.format('%s %15s %15s'% (xData[i], yData[i], zData[i])))