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
from matplotlib.ticker import MultipleLocator
from astropy.table import Table
from astroquery.vizier import Vizier

def get_vizier_data():
    """Seleccionamos del catálogo XHIP valores no nulos de:
    - Lc (clase de luminosidad)
    - B-V (índice de color)
    - VMag (magnitud absoluta visual)
    """
    v = Vizier(columns=['Lc', 'B-V', 'VMag'],
               column_filters={'Lc': '!=', 'B-V': '!=', 'VMag': '!='},
               row_limit=-1)
    result = v.query_constraints(catalog='V/137D')
    lc = result[0]['Lc'].data.data
    bv = result[0]['B-V'].data.data
    mv = result[0]['VMag'].data.data
    return lc, bv, mv

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

def plot_hr_diagram(bvlist, mvlist, lclist, colors):
    """Graficamos el diagrama HR.
    Magnitud absoluta Mv vs. índice de color B-V.
    """
    fig = plt.figure(figsize=(7, 8))
    ax = fig.add_subplot(111)
    for x, y, l, c in zip(bvlist, mvlist, lclist, colors):
        ax.scatter(x, y, c=c, s=20, label=l)
    ax.set_xlabel(r'$\mathrm{(B-V)}$', fontsize=16)
    ax.set_ylabel(r'$\mathrm{M_V}$', fontsize=16)
    ax.set_xlim(-1, 4)
    ax.set_ylim(16, -8)
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.legend()
    plt.tight_layout()
    plt.show()
    return 0

def main():
    # Tabla con el número de estrellas por clase de luminosidad
    lc, bv, mv = get_vizier_data()
    n = count_lum_class(lc)
    l = ['I', 'II', 'III', 'IV', 'V', 'VI']
    t = Table([l, n], names=('Lc', 'Num'))
    print(t)

    # Graficamos el diagrama HR:
    # diferentes colores para cada clase de luminosidad
    bvlist = [bv[lc == i] for i in np.arange(1, 7)]
    mvlist = [mv[lc == i] for i in np.arange(1, 7)]
    lclist = ['Clase I', 'Clase II', 'Clase III',
              'Clase IV', 'Clase V', 'Clase VI']
    colors = ['black', 'yellow', 'green', 'brown', 'blue', 'red']
    plot_hr_diagram(bvlist, mvlist, lclist, colors)


if __name__ == '__main__':
    main()

