### Copyright notice goes here as a comment block.

"""Overlap finds what cells a point or flight cross to find possible destinations."""
from typing import Any, Dict

import numpy as np

from flight_prediction.weighting.weighting import weighting_func, constant_weighting
from flight_prediction.grid.common import lookup_grid_index
import json
import csv

from numpy import ndarray

import tracktable
from tracktable.core.geomath import distance

def destination_dictionary(location_of_point: list, grid: np.ndarray):
    """Finds the dictionary for the latitude and longitude provided.

    Arguments:
        location_of_point (list): Latitude and longitude of a point
        grid (np.ndarray): Grid containing cells of latitudes and longitudes in the US

    Returns:
         
    """
    # Load the json file containing the grid bounds
    with open('src/flight_prediction/grid/DimensionBoundaries.json') as dimension_boundaries:
        grid_info = json.load(dimension_boundaries)

    dimensions_of_grid = len(grid.shape)

    # transform grid_info into a list of tuples of the form (min, max, step)
    grid_info = [(grid_info['lat_min'], grid_info['lat_max'], grid_info['lat_step']),
                    (grid_info['lon_min'], grid_info['lon_max'], grid_info['lon_step']),
                    (grid_info['alt_min'], grid_info['alt_max'], grid_info['alt_step']),
                    (grid_info['heading_min'], grid_info['heading_max'], grid_info['heading_step'])]

    cell_index = []

    for i in range(dimensions_of_grid):
        cell_index.append(lookup_grid_index(location_of_point[i],
                                            grid_info[i][0], grid_info[i][1], grid_info[i][2],
                                            is_heading=i == 3))

    try:
        return grid[tuple(cell_index)]
    except KeyError:
        return {}
    except IndexError:
        return {}


def flight_destination_prediction(flight, print_dict=False, grid_path=None, grid=None, weighting=False,
                                  csv_output_file=None) -> dict:
    """Finds possible destinations for a flight by finding which cell every point is in

    Arguments:
        flight (list): Flight that is being predicted
        print_dict (boolean) (optional): Prints the resulting dictionary 
        grid_path (str) (optional): Path to grid being used for prediction, used if a grid is not given to it.
        grid (dict) (optional): Grid used for the prediction. If not given a default grid is loaded.
        weighting (boolean) (optional): Weighs results from cells to get a more accurate output
        csv_output_file (str) (optional): Used to output a csv file of prediction for flight

    Returns:
        dict: keys = destination: values = destination's occurances, sorted by occurances in a percentage 
    """

    flights_overlapping_cells = {}

    x_axis = "index"    
    
    if x_axis=="index":
        divisor = len(flight)
    elif x_axis == "distance":
        divisor = distance(flight[0], flight[-1])
    elif x_axis == "time":
        divisor = (flight[0].timestamp - flight[-1].timestamp).total_seconds()
    
    if(divisor == 0):
        return flights_overlapping_cells


    # Grid containing cells of latitudes and longitudes in the US
    # containing possible destination airports for flight
    
    if grid_path is None:
        grid_path = '/anvil/projects/tdm/corporate/sandia-trajectory/data/grid_pickle_files/grid_lat_long.pkl'

    if grid is None:
        grid = np.load(grid_path, allow_pickle=True)

    # Finds cell for each point's location and adds the destination
    # into the total list of possible destinations for the flight

    dimensions_of_grid = len(grid.shape)

    list_of_cells = []
    
    for i, point in enumerate(flight):
        cell = destination_dictionary([point[1], point[0],
                                       point.properties['altitude'], point.properties['heading']], grid)
        
        if cell is not None:
            if weighting:
                # cell = constant_weighting(cell, lambda x: 2*x)
                cell = weighting_func(cell, flight, i, x_axis=x_axis)
            list_of_cells.append(cell)

    # List of cells contains all the dictionary's from each point, if weighing occured it would
    # before all of the occurances are combined 

    for cell in list_of_cells:
        flights_overlapping_cells = {x: flights_overlapping_cells.get(x, 0) +
                                        cell.get(x, 0)
                                     for x in set(flights_overlapping_cells).union(cell)}
    # The flights possible destinations are sorted by occurances

    total_flights = sum(list(flights_overlapping_cells.values()))

    if total_flights == 0:
        print("No possible destinations found")
        return {}

    # Prints out possible destinations if print_dict is true
    if print_dict:
        for key in flights_overlapping_cells:
            if flights_overlapping_cells[key] >= 1:
                print(f"{key}:{flights_overlapping_cells[key]}%")
        return flights_overlapping_cells

    if csv_output_file is not None:
        single_flight_csv_output(flights_overlapping_cells, csv_output_file)

    return flights_overlapping_cells


def multiple_flight_destination_prediction(flights: list, grid=np.ndarray, print_dict=False, weighting=False,
                                           csv_output_file=None) -> list:
    """Prediction where every flight in the file's Destination

    Arguments:
        flights (list): list of tracktable flights
        grid (np.ndarray): Grid used for the prediction. If not given a default grid is loaded.
        print_dict (boolean) (optional): Prints the resulting dictionary 
        weighting (boolean) (optional): Weighs results from cells to get a more accurate output
        csv_output_file (str) (optional): Used to output a csv file of prediction for flight

    Returns:
        list[2][# of flights]: list[0] -> trajectory for predction, list[1] -> prediction dict
    """

    list_of_predictions = []

    for flight in flights:
        # The ['Partial'] is the trajectory of the flight
        list_of_predictions.append(flight_destination_prediction(flight['Partial'], print_dict=print_dict, grid=grid,
                                                                 weighting=weighting, csv_output_file=None))
    if csv_output_file is not None:
        multiple_flight_csv_output(list_of_predictions, csv_output_file)

    return list_of_predictions


def multiple_flight_csv_output(list_of_predictions: list, csv_output_file: str):
    """Outputs the prediction for every flight in a prediction list from multiple_flight_destination_prediction()
     to a .csv file

    Arguments:
        list_of_predictions (list): list of predictions for flights from multiple_flight_destination_prediction()
        csv_output_file (str): Name for the csv file. .csv must be included  

    Returns:
        a .csv file with the name given
        Destination for flight, 1st Prediction, 2nd Predicition, 3rd Prediction... , 10th Prediction
    """

    f = open(csv_output_file, "w", newline="")
    writer = csv.writer(f)
    writer.writerow(("PR1", "PR2", "PR3", "PR4", "PR5", "PR6", "PR7", "PR8", "PR9", "PR10"))
    for flights in list_of_predictions:
        keys = list(flights.keys())
        if (len(keys) >= 10):
            result = (keys[0], keys[1], keys[2], keys[3], keys[4], keys[5],
                      keys[6], keys[7], keys[8], keys[9])
            writer.writerow(result)
    f.close()


def single_flight_csv_output(flights_overlapping_cells: dict, csv_output_file: str):
    """Outputs all the destinations found in each cell overlapped in a flight and outputs it to a .csv file 

    Arguments:
        flights_overlapping_cells (list): list of cells a flight overlapped from from flight_destination_prediction()
        csv_output_file (str): Name for the csv file. .csv must be included  

    Returns:
       None
    """
    with open(csv_output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("Destination", "Percentage of Airports Occurring"))
        for cells in flights_overlapping_cells:
            writer.writerow((cells, f"{flights_overlapping_cells[cells]}%"))


def grid_infomation(grid: dict) -> list:
    """ Generates a list of the unique latitudes and longitudes and cells from a grid

    Arguments:
        grid (dict): Cells containing a dict of destination airports

    Returns:
        List: [0] = unique latitude, [1] = unique longitudes, [2]cells 
    """
    list_of_data = list(grid.keys())
    cells = np.array(list_of_data)

    grid_latitudes = cells[:, 0]
    grid_latitudes = np.sort(np.unique(grid_latitudes))
    grid_latitude_max = grid_latitudes.max()
    grid_latitude_min = grid_latitudes.min()
    grid_latitude_step = grid_latitudes[1] - grid_latitudes[0]

    grid_longitudes = cells[:, 1]
    grid_longitudes = np.sort(np.unique(grid_longitudes))
    grid_longitude_max = grid_longitudes.max()
    grid_longitude_min = grid_longitudes.min()
    grid_longitude_step = grid_longitudes[1] - grid_longitudes[0]

    return [list_of_data, grid_latitudes, grid_longitudes, grid_latitude_max, grid_latitude_min,
            grid_latitude_step, grid_longitude_max, grid_longitude_min, grid_longitude_step]
