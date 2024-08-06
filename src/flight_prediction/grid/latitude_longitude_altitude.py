import logging
import numpy as np
import common
import json


# Create a grid of cells and count the number of airports in each cell and save the grid as a pickle file.
def main():
    dimension_boundaries = json.load(open('DimensionBoundaries.json'))
    lat_min = dimension_boundaries['lat_min']
    lat_max = dimension_boundaries['lat_max']
    lat_step = dimension_boundaries['lat_step']
    lon_min = dimension_boundaries['lon_min']
    lon_max = dimension_boundaries['lon_max']
    lon_step = dimension_boundaries['lon_step']
    alt_min = dimension_boundaries['alt_min']
    alt_max = dimension_boundaries['alt_max']
    alt_step = dimension_boundaries['alt_step']

    lat_bounds = (lat_min, lat_max, lat_step)
    long_bounds = (lon_min, lon_max, lon_step)
    alt_bounds = (alt_min, alt_max, alt_step)

    # file_path = ("/anvil/projects/tdm/corporate/sandia-trajectory/previous_files/flight/data/2023_2024"
    # "/dest_airports_small.tsv")

    # file_path = "/Users/arnavwadhwa/code/purdue/sandia-flight/histograms/gridSize/dest_airports_small.tsv"

    # dir_path = "/Users/arnavwadhwa/code/purdue/sandia-flight/2014_07_hours"

    dir_path = "/anvil/projects/tdm/corporate/sandia-trajectory/previous_files/flight/data/raw_data/fullData"

    output_file = "/anvil/projects/tdm/corporate/sandia-trajectory/data/grid_pickle_files/grid_lat_long_alt_full.pkl"

    columns = ['LATITUDE', 'LONGITUDE', 'ALTITUDE']
    target_column = 'DESTINATION_IATA'

    # grid = latitude_longitude_grid(lat_bounds, long_bounds, file_path, columns, target_column)
    grid = common.generate_grid_multiprocessing(
        dir_path, [lat_bounds, long_bounds, alt_bounds], columns, target_column, 128)

    logging.debug(grid.shape)

    # Print 100 random cells
    # for _ in range(100):
    #     cell = tuple(np.random.randint(0, s) for s in grid.shape)
    #     logging.debug(cell)
    #     logging.debug(grid[cell])

    # save the grid as a pickle file
    with open(output_file, 'wb') as f:
        np.save(f, grid)


if __name__ == "__main__":
    main()
