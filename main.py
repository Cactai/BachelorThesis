import pandas as pd
import os

from delta import Delta, Entry
from BarPlot import plotBar
from WorldPlot import plotMap
from ScatterPlot import plotScatter


def read_file(file_path : str) -> [Delta]:
    file = open(file_path, 'r')
    read_header(file)
    deltas: [Delta] = []
    while True:
        delta = read_delta(file)
        if delta is None:
            return deltas

        deltas.append(delta)


def read_header(file):
    line: str = file.readline()
    while line == len(line) * ';':
        continue

    return line.split(';')


def read_delta(file):
    line: str = file.readline().replace('\n', '')

    # EOF reached
    if line == '':
        return None

    # Skip empty rows
    while line == len(line) * ';':
        line: str = file.readline().replace('\n', '')
        continue

    # Read delta data
    delta_name = None
    delta_area = None
    information = []
    while not line == len(line) * ';':
        # Read row
        (name, period, time, area_change, error_margin, _, _, _, area) = line.split(';')[0:9]

        # Read first
        if delta_name is None:
            delta_name = name
            delta_area = area

        (start, end) = period.split('-')
        parsed_period = (int(start), int(end))

        if error_margin == '':
            parsed_error_margin = None
        else:
            parsed_error_margin = float(error_margin.replace(',', '.'))

        if area_change == '':
            parsed_area_change = None
        else:
            parsed_area_change = float(area_change.replace(',', '.'))

        information.append(Entry(parsed_period, parsed_area_change, parsed_error_margin))
        line: str = file.readline().replace('\n', '')
    return Delta(delta_name, float(delta_area.replace(',', '.')), information)


# Longitude and latitude of each delta
def read_locations(deltas: [Delta]):
    projectDir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(projectDir, "CSV", "DeltaLocations.csv"))

    for delta in deltas:
        row = df.loc[df['Name'] == delta.name]
        delta.longitude = row.Longitude.item()
        delta.latitude = row.Latitude.item()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    projectDir = os.path.dirname(__file__)
    deltas = read_file(os.path.join(projectDir, "CSV", "ExcelData.csv"))
    read_locations(deltas)

    # Generate all plots
    plotBar(deltas)
    plotMap(deltas)
    plotScatter(deltas)
