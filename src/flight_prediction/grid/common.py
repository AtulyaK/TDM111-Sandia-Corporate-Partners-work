import logging
import os.path

import numpy as np
import pandas as pd
from multiprocessing import Pool
from copy import deepcopy


def read_tsv_line_by_line(file_path: str, columns: list[str], target_column: str) -> list:
    """
    Generator to read a TSV file line by line and yields a list of the specified columns for each line.
    Args:
        file_path (str): The path to the TSV file.
        columns (list[str]): A list of column names to extract from the TSV file.
        target_column (str): The column to count the occurrences of in each cell.

    Returns:
        list: A list of the specified columns for each line in the TSV file.

    """
    usecols = columns + [target_column]
    for chunk in pd.read_csv(file_path, sep='\t', usecols=usecols, chunksize=100000):
        for index, row in chunk.iterrows():
            yield [row[column] for column in columns], row[target_column]


def create_grid_kwargs(**kwargs) -> np.ndarray:
    """
    Creates a multi-dimensional grid of cells with the number of dimensions specified in kwargs.
    Each cell is represented as an empty dictionary, and the grid allows for direct access using
    multidimensional indexing.

    Args:
        **kwargs: The dimensions of the grid in the format dimension name = (min, max, cell_size)

    Returns:
        grid: A multi-dimensional NumPy array of dictionaries, representing the grid cells.
    """
    # Determine the shape of the grid based on the provided dimensions
    dimensions = [(max_val - min_val) // cell_size for _, (min_val, max_val, cell_size) in kwargs.items()]

    # Create a multi-dimensional NumPy array of the specified shape, initialized with None
    grid_shape = tuple(dimensions)
    grid = np.empty(grid_shape, dtype=object)

    # Initialize each cell in the grid with an empty dictionary
    for index in np.ndindex(grid.shape):
        grid[index] = {}

    return grid


def example_create_grid_kwargs():
    # Example usage
    grid_kwargs = {
        'x': (0, 10, 1),
        'y': (0, 5, 1),
        'z': (0, 5, 1)
    }
    grid = create_grid_kwargs(**grid_kwargs)
    print(f"Generated grid with shape: {grid.shape}")
    # Accessing a cell (example)
    grid[0, 0, 0] = {'example': 'cell'}
    cell = grid[0][0][0]  # Accessing the first cell in each dimension

    print(f"Accessed cell: {cell}")


def create_grid_list(dimensions: list[tuple]) -> np.ndarray:
    """
    Creates a multi-dimensional grid of cells with the number of dimensions specified in the dimensions list.
    Each cell is represented as an empty dictionary, and the grid allows for direct access using
    multidimensional indexing.

    Args:
        dimensions: A list of tuples, where each tuple contains the minimum, maximum, and cell size for a dimension.

    Returns:
        grid: A multi-dimensional NumPy array of dictionaries, representing the grid cells.
    """
    # Determine the shape of the grid based on the provided dimensions
    dimensions = [(max_val - min_val) // cell_size for min_val, max_val, cell_size in dimensions]

    # Create a multi-dimensional NumPy array of the specified shape, initialized with None
    grid_shape = tuple(int(dimension) for dimension in dimensions)
    grid = np.empty(grid_shape, dtype=object)

    # Initialize each cell in the grid with an empty dictionary
    for index in np.ndindex(grid.shape):
        grid[index] = {}

    return grid


def lookup_grid_index(value: float, min_val: float, max_val: float, cell_size: float, is_heading: bool = False) -> int:
    """
    Looks up the index of a value in a grid cell based on the minimum, maximum, and cell size for the dimension.
    Args:
        value: The value to look up in the grid.
        min_val: The minimum value for the dimension.
        max_val: The maximum value for the dimension.
        cell_size: The size of each cell in the dimension.
        is_heading: A boolean indicating whether the value is a heading (wraparound from 360 to 0).

    Returns:
        index: The index of the value in the grid cell.

    """
    # index = int((value - min_val) / (max_val - min_val) * (max_val - min_val) / cell_size)

    max_index = (max_val - min_val) // cell_size

    if is_heading:
        if value < min_val or value > 360:
            # Skip the row if the value is outside the bounds
            return -1

        if 337.5 <= value <= 360:
            value = 0

        index = np.floor((value - min_val) / cell_size)
        index = int(index)

    else:
        index = np.floor((value - min_val) / cell_size)
        index = int(index)

        # To account for the floor function rounding down negative numbers
        if index < 0:
            index += 1

    if index == max_index:
        index -= 1

    return index


def fill_grid(grid, dimensions: list[tuple], columns: list, target_column: str, file_path: str) -> np.ndarray:
    """
    Fills a grid with data from a TSV file, using the specified columns and dimensions.
    Args:
        grid: Empty grid to fill with data.
        dimensions: The boundaries and cell size for each dimension in the form min, max, cell_size.
        columns: The column headers to read from the TSV file.
        target_column: The column to count the occurrences of in each cell.
        file_path: The path to the TSV file containing the data.
    Returns:
        grid: A grid of dictionaries containing the data from the TSV file.
    """
    if len(dimensions) != len(grid.shape):
        raise ValueError("The number of dimensions in the grid does not match the number of dimensions specified.")

    if len(columns) != len(dimensions):
        raise ValueError("The number of columns does not match the number of dimensions specified.")

    for row, target in read_tsv_line_by_line(file_path, columns, target_column):
        indices = []
        logging.debug(f"Row: {row}")
        for i, (min_val, max_val, cell_size) in enumerate(dimensions):
            value = row[i]

            if isinstance(value, str) or np.isnan(value):
                # Skip the row if the value is NaN
                logging.debug(f"Skipping row {row} because value is NaN")
                break

            index = lookup_grid_index(value, min_val, max_val, cell_size, columns[i] == 'HEADING')

            if index < 0 or index >= grid.shape[i]:
                # Skip the row if the value is outside the bounds
                logging.debug(f"Skipping row {row} because value is outside the bounds")
                break
            indices.append(index)
        else:
            # If the loop completes without breaking, fill the cell in the grid
            grid[tuple(indices)][target] = grid[tuple(indices)].get(target, 0) + 1

    return grid


def merge_grids(grids: list[np.ndarray]) -> np.ndarray:
    """
    Merges a list of grids into a single grid by summing the values of the dictionaries in each cell.
    Args:
        grids: A list of grids to merge.

    Returns:
        grid: A single grid containing the merged data from all the input grids.

    """

    # Choose the first grid as the base grid to merge the other grids into
    grid = grids[0]

    grids.remove(grids[0])

    # Sum the values of the dictionaries in each cell from all the input grids
    for grid_ in grids:
        for index in np.ndindex(grid.shape):
            for key, value in grid_[index].items():
                grid[index][key] = grid[index].get(key, 0) + value

    return grid


def generate_grid_multiprocessing(directory_path: str, grid_dimensions: list[tuple], columns: list[str],
                                  target_column: str, num_processes: int) -> np.ndarray:
    """
    Generate a grid from a directory of files using multiprocessing.
    Args:
        directory_path: The path to the directory containing the files.
        grid_dimensions: The boundaries and cell size for each dimension.
        columns: The column headers to read from the TSV file.
        target_column: The column to count the occurrences of in each cell.
        num_processes: The number of processes to use for multiprocessing.

    Returns:
        grid: A grid of dictionaries containing the data from the TSV files in the directory.

    """
    empty_grid = create_grid_list(grid_dimensions)

    # Spawn a process for each file in the directory up to the number of processes
    # and fill the grid with the data from the files

    files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.tsv')]

    with Pool(num_processes) as pool:
        results = pool.starmap(fill_grid, [(deepcopy(empty_grid), grid_dimensions, columns, target_column, file)
                                           for file in files])

    return merge_grids(results)


if __name__ == '__main__':
    example_create_grid_kwargs()
