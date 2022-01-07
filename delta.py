import numpy as np


# Holding data for the delta
class Delta:
    def __init__(self, delta_name, delta_area, information):
        self.name: str = delta_name
        self.longitude, self.latitude = None, None
        self.information: [Entry] = information
        self.standard_error, self.standard_deviation, self.mean = None, None, None
        self.area: float = delta_area / 1000000  # Convert to km^2
        self.calc_standard_deviation()

    def __str__(self) -> str:
        return f'{self.name} Mean: {self.mean} SD:{self.standard_deviation} SE:{self.standard_error}'

    def calc_standard_deviation(self) -> (float, float):
        area_change = [entry.area_change for entry in self.information if entry.area_change]
        self.standard_deviation: float = np.std(area_change, ddof=1)
        self.standard_error: float = self.standard_deviation / np.sqrt(len(area_change))
        self.mean: float = np.mean(area_change)


# A measurement entry
class Entry:
    def __init__(self, period, area_change, error_margin):
        self.period: (int, int) = period
        self.area_change: float = area_change
        self.error_margin: float = error_margin

    def __str__(self):
        return f'T: ({self.period[0]}-{self.period[1]}) Mean: {self.mean} ΔArea: {self.area_change} Error_margin: {self.error_margin}'
