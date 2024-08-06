import pandas as pd
import os
import os.path
from tracktable.domain.terrestrial import TrajectoryPointReader
from tracktable.applications.assemble_trajectories import AssembleTrajectoryFromPoints
from tracktable.domain.terrestrial import TrajectoryWriter
import datetime
import logging
import sys

"""
This file converts csv files to traj files.
"""


def csv_to_traj(input_file, traj_file):
    """
    Converts a csv file to a traj file.

    Arguments:
        csv_file - the path to the csv file that should be converted
        traj_file - the path where the new traj file should be written to
    """

    with open(input_file, 'r') as inFile:
        reader = TrajectoryPointReader()
        reader.input = inFile
        reader.comment_character = '#'

        # Determine file extension for setting the appropriate field delimiter
        file_extension = os.path.splitext(input_file)[1]
        if file_extension == ".tsv":
            reader.field_delimiter = '\t'
        elif file_extension == ".csv":
            reader.field_delimiter = ","

        # Setup columns for trajectory point reader
        setup_trajectory_point_reader(reader)

        builder = AssembleTrajectoryFromPoints()
        builder.input = reader
        builder.minimum_length = 10
        builder.separation_time = datetime.timedelta(minutes=30)
        traj = list(builder.trajectories())

    with open(traj_file, 'wb') as trajectory:
        writer = TrajectoryWriter(trajectory)
        writer.write(traj)

    del traj  # Free up memory


def setup_trajectory_point_reader(reader):
    """
    Sets up the trajectory point reader with predefined column mappings.
    This is separated from the main function to improve readability.
    """
    reader.object_id_column = 0
    reader.timestamp_column = 1
    reader.coordinates[1] = 3
    reader.coordinates[0] = 2
    reader.set_real_field_column('speed', 4)
    reader.set_real_field_column('heading', 5)
    reader.set_real_field_column('altitude', 6)
    reader.set_string_field_column('origin', 25)
    reader.set_string_field_column('destination', 30)


def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Check for the correct number of arguments
    if len(sys.argv) != 3:
        logger.error("Usage: csv_to_traj.py input_file.csv output_file.traj")
        return 1

    # Get the input and output file paths
    data_input = sys.argv[1]
    data_output = sys.argv[2]

    if os.path.isdir(data_input):
        # If the output dir doesn't exist, create it
        if not os.path.exists(data_output):
            os.makedirs(data_output)

        # Iterate through the input directory and convert each file keeping the full path of the file
        for root, dirs, files in os.walk(data_input):
            for file in files:
                if file.endswith(".csv") or file.endswith(".tsv"):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(data_output, file[:-4] + ".traj")
                    csv_to_traj(input_file, output_file)

    else:
        csv_to_traj(data_input, data_output)

    return 0


if __name__ == '__main__':
    sys.exit(main())
