import logging
import numpy as np
import common
import json


def latitude_longitude_grid(lat_bounds: tuple[float, float, float], long_bounds: tuple[float, float, float],
                            file_path: str, columns: list[str], target_column: str) -> np.ndarray:
    """
    Create a grid of cells and count the number of airports in each cell and save the grid as a pickle file.
    Args:
        lat_bounds: A tuple of floats representing the minimum, maximum latitude values and the cell size.
        long_bounds: A tuple of floats representing the minimum and maximum longitude values and the cell size.
        file_path:  A string representing the file path of the data.
        columns: A list of strings representing the columns to be read from the file.
        target_column: A string representing the column to count the occurrences of in each cell.

    Returns:
        grid: A grid of dictionaries containing the airport counts for each cell

    """
    # Create the grid as an n-dimensional array with axes
    grid = common.create_grid_list([lat_bounds, long_bounds])

    # Read the data from the file
    grid = common.fill_grid(grid, [lat_bounds, long_bounds], columns, target_column, file_path)

    return grid


def main():
    # Define the grid bounds
    dimension_boundaries = json.load(open('DimensionBoundaries.json'))
    lat_min = dimension_boundaries['lat_min']
    lat_max = dimension_boundaries['lat_max']
    lat_step = dimension_boundaries['lat_step']
    lon_min = dimension_boundaries['lon_min']
    lon_max = dimension_boundaries['lon_max']
    lon_step = dimension_boundaries['lon_step']

    lat_bounds = (lat_min, lat_max, lat_step)
    long_bounds = (lon_min, lon_max, lon_step)

    # file_path = ("/anvil/projects/tdm/corporate/sandia-trajectory/previous_files/flight/data/2023_2024"
                 # "/dest_airports_small.tsv")

    # file_path = "/Users/arnavwadhwa/code/purdue/sandia-flight/histograms/gridSize/dest_airports_small.tsv"

    # dir_path = "/Users/arnavwadhwa/code/purdue/sandia-flight/2014_07_hours"

    dir_path = "/anvil/projects/tdm/corporate/sandia-trajectory/previous_files/flight/data/raw_data/fullData"

    output_file = "/anvil/projects/tdm/corporate/sandia-trajectory/data/grid_pickle_files/grid_lat_long_full.pkl"

    columns = ['LATITUDE', 'LONGITUDE']
    target_column = 'DESTINATION_IATA'

    # grid = latitude_longitude_grid(lat_bounds, long_bounds, file_path, columns, target_column)
    grid = common.generate_grid_multiprocessing(dir_path, [lat_bounds, long_bounds], columns, target_column, 128)
    logging.debug(grid.shape)

    # Print 100 random cells
    for _ in range(100):
        logging.debug(grid[tuple(np.random.randint(0, s) for s in grid.shape)])

    # save the grid as a pickle file
    with open(output_file, 'wb') as f:
        np.save(f, grid)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    main()


