import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid.inset_locator import zoomed_inset_axes, mark_inset
from mpl_toolkits.axes_grid.anchored_artists import AnchoredSizeBar

from delta import Delta


# Worldplot with delta size
def plotMap(deltas: [Delta]):
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes()

    # Worldplot
    bmap = Basemap(ax=ax, resolution='i',
                   llcrnrlat=-40, llcrnrlon=-145,
                   urcrnrlat=75, urcrnrlon=145)

    bmap.shadedrelief()

    # Ticks
    bmap.drawmeridians(np.arange(-140, 160, 20), labels=[False, False, False, True])
    bmap.drawparallels(np.arange(-30, 90, 20), labels=[True, False, False, False])

    # Information
    longitudes = [delta.longitude for delta in deltas]
    latitudes = [delta.latitude for delta in deltas]
    names = [delta.name for delta in deltas]

    # To make them more visible on the map
    multipliedSizes = [2*delta.standard_deviation for delta in deltas]

    x, y = bmap(longitudes, latitudes)

    # Dots on the map
    bmap.scatter(x, y, c='red', s=multipliedSizes, label=names)

    # Title and show
    plt.title("Delta area change standard deviation")
    plt.show()


if __name__ == '__main__':
    plotMap([])
