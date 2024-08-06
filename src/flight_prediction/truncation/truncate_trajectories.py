import argparse
import random
import sys
from datetime import timedelta
import numpy as np
from tracktable.domain.terrestrial import TrajectoryReader
import tracktable.core.geomath as geomath
import pickle

"""
This program truncates the trajectories based on our goals; 
for initial testing, it will truncate them at 95% and 70%.
"""


def truncate_single_flight(flight, percent: float) -> dict:
    """
    Truncates a single flight at a certain percentage by time.

    Args:
       flight (tracktable trajectory): the flight to be truncated as
       percent:

   Returns:
       dict: keys = origin, destination, full trajectory, truncated trajectory, and Percent

   """

    truncated_flight_dict = {}

    start_time_of_flight = flight[0].timestamp
    end_time_of_flight = flight[-1].timestamp
    time_difference = end_time_of_flight - start_time_of_flight
    time_difference = time_difference.total_seconds()
    truncated_flight_duration = time_difference * percent

    time_to_remove = time_difference - truncated_flight_duration

    truncated_flight_start_time = start_time_of_flight + timedelta(seconds=time_to_remove / 2)
    truncated_flight_end_time = end_time_of_flight - timedelta(seconds=time_to_remove / 2)

    truncated_flight = geomath.subset_during_interval(flight, truncated_flight_start_time, truncated_flight_end_time)

    # Add the metadata to the truncated flight

    # Get the origin and destination
    origin = None
    destination = None

    for point in flight:
        if point.properties['origin'] is not None:
            origin = point.properties['origin']

        if point.properties['destination'] is not None:
            destination = point.properties['destination']

        if origin is not None and destination is not None:
            break

    if origin is None:
        origin = "Unknown"

    if destination is None:
        return {}

    # Add the origin and destination to the truncated flight
    truncated_flight_dict["Origin"] = origin
    truncated_flight_dict["Destination"] = destination
    truncated_flight_dict["Full"] = flight
    truncated_flight_dict["Partial"] = truncated_flight
    truncated_flight_dict["Percent"] = percent

    return truncated_flight_dict


def truncate_flight_by_traj_file(trajectories: list, percent_range: tuple) -> list:
    """
    Truncates a flight by traj file at a certain percentage by time.

    Args:
       trajectories (list): the list of trajectories to be truncated
       percent_range (tuple): the range of percentages to truncate the flights at in the form of (min, max_ or
         (min, max, step). If step is not given, it defaults to 5.

    Returns:
         list: list of truncated flights
     """

    if len(percent_range) == 2:
        percent_range = (percent_range[0], percent_range[1], 5)

    percentages = np.arange(percent_range[0], percent_range[1], percent_range[2])

    truncated_flights = []
    for trajectory in trajectories:
        percent = random.choice(percentages)
        truncated_flight = truncate_single_flight(trajectory, percent)
        if truncated_flight:
            truncated_flights.append(truncated_flight)

    return truncated_flights


def truncate(traj_file: str, pickle_path: str, percent_range: tuple) -> None:
    """
    Truncates a traj file at a certain percentage by time and saves the truncated flights to a pickle file.

    Args:
       traj_file (str): the traj file to be truncated
       pickle_path (str): the path to save the pickle file
       percent_range (tuple): the range of percentages to truncate the flights at in the form of (min, max_ or
         (min, max, step). If step is not given, it defaults to 5.

    Returns:
         None
     """

    with open(traj_file, 'rb') as file:
        reader = TrajectoryReader()
        reader.input = file
        trajectories = list(reader)

    truncated_flights = truncate_flight_by_traj_file(trajectories, percent_range)

    # Save the truncated flights to a pickle file
    with open(pickle_path, 'wb') as file:
        pickle.dump(truncated_flights, file)
        print(f"Truncated flights saved to {pickle_path}")

    return None


def main():
    parser = argparse.ArgumentParser(description='Truncate a traj file at a certain percentage by time and save the '
                                                 'truncated flights to a pickle file.')

    parser.add_argument("traj_file", type=str, help='Path to traj file.', nargs='?')
    parser.add_argument("pickle_path", type=str, help='Path to save the pickle file.', nargs='?')
    parser.add_argument("min_percent", type=float, help="Minimum percentage", default=0.05, nargs='?')
    parser.add_argument("max_percent", type=float, help="Maximum percentage", default=0.8, nargs='?')
    parser.add_argument("step_percent", type=float, help="Step percentage", default=0.05, nargs='?')

    args = parser.parse_args()

    print(f"Truncating {args.traj_file} at {args.min_percent} to {args.max_percent} by {args.step_percent} and saving "
          f"to {args.pickle_path}")

    percent_range = (args.min_percent, args.max_percent, args.step_percent)

    truncate(args.traj_file, args.pickle_path, percent_range)


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.CRITICAL + 1)
    main()
    # truncate("2013_05_02_20.traj", "truncated_flights.pkl", (0.05, 0.8, 0.05))
    sys.exit(0)
