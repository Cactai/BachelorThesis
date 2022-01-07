import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import Locator
from delta import Delta


def plotBar(deltas: [Delta]):
    values = [delta.mean for delta in deltas]
    names = [delta.name for delta in deltas]
    error = [delta.standard_error for delta in deltas]

    # Plot
    fig, ax = plt.subplots(1, 1)
    bars = ax.bar(names, values, y=0, yerr=error)

    # Ticks
    ax.set_xticklabels(names, rotation=45, fontsize=8, va='top', ha='right')
    plt.title('Change in area delta')
    plt.ylabel('Area Change (km^2/year)')
    plt.xlabel('Delta name')

    # Everything for y axis + grid
    plt.yscale('symlog')
    plt.grid(True, which="both", axis='y')
    yaxis = plt.gca().yaxis
    yaxis.set_minor_locator(MinorSymLogLocator(1e-1))
    ax.set_axisbelow(True)

    # Plot properties and show
    fig.set_figwidth(10)
    fig.subplots_adjust(bottom=0.3)
    plt.show()


# Source: https://stackoverflow.com/questions/20470892/how-to-place-minor-ticks-on-symlog-scale
class MinorSymLogLocator(Locator):
    """
    Dynamically find minor tick positions based on the positions of
    major ticks for a symlog scaling.
    """
    def __init__(self, linthresh):
        """
        Ticks will be placed between the major ticks.
        The placement is linear for x between -linthresh and linthresh,
        otherwise its logarithmically
        """
        self.linthresh = linthresh

    def __call__(self):
        'Return the locations of the ticks'
        majorlocs = self.axis.get_majorticklocs()
        # my changes to previous solution
        # this adds one majortickloc below and above the axis range
        # to extend the minor ticks outside the range of majorticklocs
        # bottom of the axis (low values)
        first_major = majorlocs[0]
        if first_major == 0:
            outrange_first = -self.linthresh
        else:
            outrange_first = first_major * float(10) ** (- np.sign(first_major))
        # top of the axis (high values)
        last_major = majorlocs[-1]
        if last_major == 0:
            outrange_last = self.linthresh
        else:
            outrange_last = last_major * float(10) ** (np.sign(last_major))
        majorlocs = np.concatenate(([outrange_first], majorlocs, [outrange_last]))
        # iterate through minor locs
        minorlocs = []

        # handle the lowest part
        for i in range(1, len(majorlocs)):
            majorstep = majorlocs[i] - majorlocs[i-1]
            if abs(majorlocs[i-1] + majorstep/2) < self.linthresh:
                ndivs = 10
            else:
                ndivs = 9
            minorstep = majorstep / ndivs
            locs = np.arange(majorlocs[i-1], majorlocs[i], minorstep)[1:]
            minorlocs.extend(locs)

        return self.raise_if_exceeds(np.array(minorlocs))
