import numpy as np
import matplotlib.pyplot as plt

from delta import Delta


# Scatter plot putting area vs deviation
def plotScatter(deltas: [Delta]):
    fig, ax = plt.subplots(1, 1)

    areas = [delta.area for delta in deltas]
    deviation = [delta.standard_deviation for delta in deltas]

    z = np.polyfit(areas, deviation, 1)
    p = np.poly1d(z)
    ax.plot(areas, p(areas), color='red', linestyle='dashed', markersize=12)
    ax.scatter(x=areas, y=deviation)

    plt.title("Error in annual delta area change")
    plt.ylabel('Standard deviation (km^2)')
    plt.xlabel('Delta area (km^2)')
    plt.show()
