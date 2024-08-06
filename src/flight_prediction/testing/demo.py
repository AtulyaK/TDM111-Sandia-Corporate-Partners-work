"""Test overlap.py with single or multiple flights."""

import flight_prediction.overlapping
import numpy as np

def demo_multiple_flights(file_name: str):
    """Runs overlap.py with multple flights

    Arguments:
        file (str): file containing multiple trajectories
    Returns:
        print results on all of predications
    """
    flight_file = np.load(file_name, allow_pickle=True)
    #Results stores how good a prediction was, result[0]: First result in dict, result[1]: Top 3 but not #1, 
    #results[2]: In the dict but not top 3, results[3], not in dict
    results = [0,0,0,0]
    num_flights = len(flight_file)
    flight_predictions = flight_prediction.overlapping.multiple_flight_destination_prediction(file_name,True, weighting = True)
    for flights in flight_predictions:
        destination = flights[0]["Destination"][1::]
        airport_number = 1
        flight_found = False
        prediction_list = list(flights[1].items())
        prediction_list = sorted(prediction_list, key=lambda prediction_list: prediction_list[1], reverse=True)
        for key in prediction_list:
            if destination == key[0]:
                flight_found = True
                if airport_number == 1:
                    results[0] += 1
                elif airport_number <= 3:
                    results[1] += 1
                else:
                    results[2] += 1
            airport_number += 1
        if flight_found is False: 
            results[3] += 1

    print(f"{(results[0]/num_flights)*100:.2f}% of predictions had the correct"
           " destination as the first option")
    print(f"{(results[1]/num_flights)*100:.2f}% of predictions had the correct"
          " destination not as the first option but in the top 3")
    print(f"{(results[2]/num_flights)*100:.2f}% of predictions had the correct"
           " destination not in the top 3 but as a option")
    print(f"{(results[3]/num_flights)*100:.2f}% of predictions did not have the"
          " correct destination as a option")




def demo_single_flight(flight : list):
    """Runs overlap.py over a single flight

    Arguments:
        flight (list): list of points in a flight
    Returns:
        print predicted destinations
    """
    length = len(flight["Partial"])
    origin = flight["Origin"][0::]
    destination = flight["Destination"][0::]
    print(f"This flight originated at {origin} and landed at {destination} with "
          f"with {length} points")
    flight_prediction.overlapping.flight_destination_prediction(flight["Partial"], True)

