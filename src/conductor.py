"""This script will complete the entire process diagram.

Execute this file by running 'python3 conductor.py' from the src/ directory.
"""

# Python packages to import
import sys
import os
import logging
import numpy as np
import argparse
import random
from datetime import datetime
import matplotlib.pyplot as plt


# Our packages to import
import flight_prediction
from flight_prediction import conductor_external
import flight_prediction.exploration
import flight_prediction.filtering
import flight_prediction.truncation
import flight_prediction.grid
from flight_prediction.overlapping import flight_destination_prediction, multiple_flight_destination_prediction
import flight_prediction.weighting
from flight_prediction import visualization

# Define the logging level
logging.getLogger().setLevel(logging.DEBUG)
  
# Where the magic is made
def main():

    parser = argparse.ArgumentParser(description='Predict the destination of a flight using a grid.')
    parser.add_argument("flights_path", type=str, nargs="?", help='Path to truncated flights file.',
                        default="/anvil/projects/tdm/corporate/sandia-trajectory/previous_files/flight/data/2023_2024"
                                "/truncatedTrajectories/2013-04-01.pkl")
    parser.add_argument('grid_path', type=str, nargs="?", help='Path to grid file.',
                        default="/anvil/projects/tdm/corporate/sandia-trajectory/data/grid_pickle_files/"
                                "grid_lat_long.pkl")

    args = parser.parse_args()

    logging.info('Testing overlapping cells with a single truncated flight while weighing it and generating a csv file')
    flights = np.load(args.flights_path, allow_pickle=True)
    #flights = random.sample(list(flights), 200)
    print(f"File contains {len(flights)} flights")
    
    grid = np.load(args.grid_path, allow_pickle=True)

    logging.info('Testing overlapping cells with multiple truncated flights with weighting,'
                 ' generating a .csv file and gives a accuracy on the flights')
    list_of_predictions = multiple_flight_destination_prediction(flights=flights, grid=grid,
                                                                 weighting=False)
    #top x for file writing at end
    top_prediction = 0
    top_three_prediction = 0
    top_ten_prediction = 0
    top_20_prediction = 0
    skipped_predictions = 0
    #the number of flights
    number_of_flights = len(list_of_predictions)
    #file name outputs
    path = "/anvil/projects/tdm/corporate/sandia-trajectory/data/output_files/test_data_generation_conductor/"
    output_file_name = os.path.join(path, "txt_folder/",conductor_external.timestamp_to_string(datetime.now(),True,False))
    output_file_name_csv = os.path.join(path, "csv_overall/" ,conductor_external.timestamp_to_string(datetime.now(),False,True))
    output_file_name_graph = os.path.join(path, "graphs_folder/" ,conductor_external.timestamp_to_string(datetime.now(),False,True))
    output_file_name_confusion_matrix = os.path.join(path, "csv_confusion_matrix/" ,conductor_external.timestamp_to_string(datetime.now(),False,True))
    output_file_visualization_path = os.path.join(path, f"graphs_folder/{conductor_external.timestamp_to_string(datetime.now(),False,False)}")
    os.mkdir(output_file_visualization_path)
    #percent removed and top x lists for csv+graph output
    percent = [.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6,.65,.7,.75]
    percent_placement_dict = {
      "Top 1" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "Top 3" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "Top 10" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      "Top 20" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    }
    #confusion matrix dictionary:
    # {"actual":"predicted"} : "# of occurences"
    confusion_matrix_dict = {}
    #Set up the txt file for writing
    conductor_external.setup(output_file_name)
    # Compare the prediction to the actual destination
    for flight, prediction in zip(flights, list_of_predictions):
      destination = flight['Destination'][1:]
      #writes destination and percentage to flight
      conductor_external.destination_write(output_file_name, destination,round(flight['Percent'],2))
      # Checks if the dict returned by the overlapping method is empty
      if not prediction:
          skipped_predictions += 1
          continue
      # Sort the dictionary by value and get the list of destinations
      list_of_possible_destinations = sorted(prediction.items(), key=lambda item: item[1], reverse=True)
      # Goes through the entire list of destinations and adds them to the right lists based on the results
      for i, predicted_destination in enumerate(list_of_possible_destinations):
        #appends/increments actual vs predicted to confusion matrix
        key = (destination,predicted_destination[0])
        if key in confusion_matrix_dict and i == 0:
          confusion_matrix_dict[key] += 1
        elif key not in confusion_matrix_dict and i == 0:
          confusion_matrix_dict[key] = confusion_matrix_dict.get(key, 0) + 1
        #adds top 20 predicted airports to the text files
        if i < 20:
          conductor_external.destination_predicted(output_file_name, i+1, predicted_destination)
        #the next 4 ifs check if the values are in the top 1,3,10,20
        if i == 0 and predicted_destination[0] == destination:
          top_prediction += 1
          percent_placement_dict['Top 1'][percent.index(round(flight['Percent'],2))] += 1
        if i < 3 and predicted_destination[0] == destination:
          top_three_prediction += 1
          percent_placement_dict['Top 3'][percent.index(round(flight['Percent'],2))] += 1
        if i < 10 and predicted_destination[0] == destination:
          top_ten_prediction += 1
          percent_placement_dict['Top 10'][percent.index(round(flight['Percent'],2))] += 1
        if i < 20 and predicted_destination[0] == destination:
          top_20_prediction += 1
          percent_placement_dict['Top 20'][percent.index(round(flight['Percent'],2))] += 1
      #pass prediction dictionary to Ishaan A's function
      #visualization.draw_airports([i[0] for i in list_of_possible_destinations], flight['Origin'],f"{output_file_visualization_path}")
    #average each value of the top x per percentage remaining
    for i,j in enumerate(percent):
      sum_list = (percent_placement_dict['Top 1'][i] + percent_placement_dict['Top 3'][i] + percent_placement_dict['Top 10'][i] + 
                  percent_placement_dict['Top 20'][i])
      if sum_list != 0:
        percent_placement_dict['Top 1'][i] = percent_placement_dict['Top 1'][i]/sum_list
        percent_placement_dict['Top 3'][i] = percent_placement_dict['Top 3'][i]/sum_list
        percent_placement_dict['Top 10'][i] = percent_placement_dict['Top 10'][i]/sum_list
        percent_placement_dict['Top 20'][i] = percent_placement_dict['Top 20'][i]/sum_list 
    #line graph of output
    conductor_external.line_graph(output_file_name_graph, percent, percent_placement_dict)
    #confusion matrix dictionary to numpy conversion
    conductor_external.confusion_matrix_csv(output_file_name_confusion_matrix, confusion_matrix_dict)
    #file write stuff to move to function
    overall_prediction = top_prediction + top_three_prediction + top_ten_prediction + top_20_prediction
    conductor_external.overall_txt_output(output_file_name, 1, top_prediction, number_of_flights, skipped_predictions)
    conductor_external.overall_txt_output(output_file_name, 3, top_three_prediction, number_of_flights, skipped_predictions)
    conductor_external.overall_txt_output(output_file_name, 10, top_ten_prediction, number_of_flights, skipped_predictions)
    conductor_external.overall_txt_output(output_file_name, 20, top_20_prediction, number_of_flights, skipped_predictions)
    conductor_external.overall_txt_output(output_file_name, "Overall", overall_prediction, number_of_flights, skipped_predictions)
    #Overall CSV output
    total_flights_with_prediction = number_of_flights - skipped_predictions
    conductor_external.overall_csv(output_file_name_csv, top_prediction, skipped_predictions, number_of_flights, 
                                 total_flights_with_prediction, top_three_prediction, top_ten_prediction, top_20_prediction)
    return 0


# What to do when the script is called
if __name__ == '__main__':
    import cProfile

    # cProfile.run('main()', sort='tottime')
    main()
