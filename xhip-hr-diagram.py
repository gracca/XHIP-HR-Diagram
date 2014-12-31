#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# xhip-hr-diagram.py
#
# Copyright (C) 2014 Germán A. Racca
# E-Mail: <gracca[AT]gmail[DOT]com>
# License: GPLv3+


"""
Construcción del diagrama de Hertszprung-Russell (HR)
XHIP: An Extended Hipparcos Compilation
      Anderson E., Francis C.
      <Astron. Letters 38 (2012)>
http://cdsads.u-strasbg.fr/abs/2012AstL...38..331A
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from astropy.table import Table
from astroquery.vizier import Vizier


def get_vizier_data():
    """Seleccionamos del catálogo XHIP valores no nulos de:
    - Lc (clase de luminosidad)
    - B-V (índice de color)
    - VMag (magnitud absoluta visual)
    - SpType (tipo espectral)
    """
    v = Vizier(columns=['Lc', 'B-V', 'VMag', 'SpType'],
               column_filters={'Lc': '!=', 'B-V': '!=',
                               'VMag': '!=', 'SpType': '!='
                               },
               row_limit=-1)
    result = v.query_constraints(catalog='V/137D')
    lc = result[0]['Lc'].data.data
    bv = result[0]['B-V'].data.data
    mv = result[0]['VMag'].data.data
    sp = result[0]['SpType'].data.data
    return lc, bv, mv, sp


def count_lum_class(lc):
    """Clasificamos las estrellas en clase de luminosidad.
    Codificación de VizieR:
    1 = I, 2 = II, 3 = III, 4 = IV, 5 = V, 6 = VI
    """
    lum = lc.tolist()
    cls = np.arange(1, 7)
    num = []
    for i in cls:
        num = np.append(num, lum.count(i))
    return num


def count_sp_type(sp):
    """Clasificamos las estrellas según el tipo espectral MK:
    O, B, A, F, G, K y M
    """
    spt = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    spl = [i[:1] for i in sp.tolist()]
    num = []
    for i in spt:
        num = np.append(num, spl.count(i))
    return num, spt


def plot_hr_diagram(bvlist, mvlist, lclist, colors):
    """Graficamos el diagrama HR.
    Magnitud absoluta Mv vs. índice de color B-V.
    """
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111)
    for x, y, l, c in zip(bvlist, mvlist, lclist, colors):
        ax.scatter(x, y, c=c, s=30, label=l, alpha=0.5, edgecolors='none')
    ax.set_xlabel(r'$\mathregular{(B-V)}$', fontsize=16)
    ax.set_ylabel(r'$\mathregular{M_V}$', fontsize=16)
    ax.set_xlim(-1, 4)
    ax.invert_yaxis()
    ax.grid(ls='-', c='gray', alpha=0.5)
    ax.legend(markerscale=1.25, fancybox=True, shadow=True)
    bbox_props = dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9)
    ax.text(1.5, 17, 'Diagrama de Hertszprung-Russell', ha='center',
            va='center', size=20, bbox=bbox_props)
    plt.tight_layout()
    plt.show()
    return 0


def main():
    # Generamos los datos
    lc, bv, mv, sp = get_vizier_data()

    # Tabla con el número de estrellas por clase de luminosidad
    n = count_lum_class(lc)
    l = ['I', 'II', 'III', 'IV', 'V', 'VI']
    t = Table([l, n], names=('Lc', 'Num'))
    print(t)
    print('')

    # Tabla con el número de estrellas por tipo espectral
    n, s = count_sp_type(sp)
    t = Table([s, n], names=('SpT', 'Num'))
    print(t)

    # Graficamos el diagrama HR:
    # diferentes colores para cada clase de luminosidad
    bvlist = [bv[lc == i] for i in np.arange(1, 7)]
    mvlist = [mv[lc == i] for i in np.arange(1, 7)]
    lclist = ['Clase I', 'Clase II', 'Clase III',
              'Clase IV', 'Clase V', 'Clase VI']
    colors = ['black', 'yellow', 'green', 'orange', 'blue', 'red']
    plot_hr_diagram(bvlist, mvlist, lclist, colors)


if __name__ == '__main__':
    main()
