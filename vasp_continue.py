"""
The script updates the INCAR MAGMOM line and POSCAR file.

The script is run as a command line program. See:
    $ python vasp_continue.py

The following files are required in the working directory:
    - INCAR
    - OUTCAR
    - CONTCAR

Author: James T. Pegg

"""

import os


def magmom_line():
    """
    Create MAGMOM line from OUTCAR.

    Returns
    ---------
    e_magmom: :class:`str`
        The updated MAGMOM line.

    """
    xData = []
    xmTitle = xmStart = xmEnd = 0

    yData = []
    ymTitle = ymStart = ymEnd = -1

    zData = []
    zmTitle = zmStart = zmEnd = -1

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
            if ('tot' in line) and (n >= xmStart):
                xmEnd = n - 2
                break

    with open('OUTCAR', 'r+') as f:
        for n, line in enumerate(f):
            if ('tot ' in line) and (n >= ymStart) and (ymStart != -1):
                ymEnd = n - 2
                break

    with open('OUTCAR', 'r+') as f:
        for n, line in enumerate(f):
            if ('tot ' in line) and (n >= zmStart) and (zmStart != -1):
                zmEnd = n - 2
                break

    with open('OUTCAR', 'r+') as f:
        for n, line in enumerate(f):
            if (n >= xmStart) and (n <= xmEnd):
                xData.append(line.split()[5])
            if (n >= ymStart) and (n <= ymEnd):
                yData.append(line.split()[5])
            if (n >= zmStart) and (n <= zmEnd):
                zData.append(line.split()[5])

    l_magmom = 'MAGMOM = '
    for i in range(0, len(xData)):
        if len(xData) == len(yData) == len(zData):
            p_magmom = str(xData[i]) + ' ' + str(yData[i]) + ' ' + str(zData[i]) + '   '
            l_magmom = l_magmom + p_magmom
        else:
            p_magmom = str(xData[i]) + '   '
            l_magmom = l_magmom + p_magmom

    e_magmom = l_magmom[:-3]
    return e_magmom


def update_incar(e_magmom):
    """
    Updates the INCAR MAGMOM keyword.

    Parameters
    ----------
    e_magmom: :class:`str`
        The updated MAGMOM line.

    Returns
    -------
    None: :class:`NoneType`

    """
    with open('INCAR', 'r') as incar, open('MAGCAR', 'w') as magcar:
        for line in incar:
            if 'MAGMOM' in line:
                magcar.write(e_magmom + '\n')
            else:
                magcar.write(line)

    os.rename('MAGCAR', 'INCAR')

def main():
    e_magmom = magmom_line()
    update_incar(e_magmom=e_magmom)
    os.rename('CONTCAR', 'POSCAR')

if __name__ == '__main__':
    main()
