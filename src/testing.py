### Copyright notice goes here as a comment block

"""This script will complete the entire process diagram.
    Students: Atulya, Connor, Kush, and Bryce.
    
    Functionality: The goal is to have a closed system to test the entire process's success.
    
    Returns: nothing. A text file is generated with the results. Look for that as it 
    will be named the same as the generated pickle file except with a .txt extension
    replacing the .pickle extension.

Execute this file by running 'python3 testing.py' from the src/ directory.
"""

# Python packages to import
import sys
import time
import logging
import numpy as np
import random

# Our packages to import
import flight_prediction
import flight_prediction.exploration
import flight_prediction.filtering
import flight_prediction.truncation
import flight_prediction.grid
import flight_prediction.overlapping
import flight_prediction.weighting

# Define the logging level
logging.getLogger().setLevel(logging.DEBUG)

# Where the magic is made
def main():
    logging.info('Testing say_hello function:')
    flight_prediction.say_hello()
    
    logging.info('Testing a file in a sub-directory')
    flight_prediction.truncation.test()

    logging.info('Testing overlapping cells with a truncated flight')
    path = "/anvil/projects/tdm/corporate/sandia-trajectory/data/major5_rem25.pickle"
    #change to use with open("flie_path",w) as file_write
    #make file writing more defensive
    f = np.load(path, allow_pickle=True)
    file_name = path[0:path.index("major5_rem25.pickle") - 1] + "/major5_rem25.txt"
    print(file_name)
    
    file_write = open(file_name, "w")
    file_write.write("Output of the truncated flights:\n")
    file_write.write("\n\n\n\n\n")
    first_prediction = 0
    top_three = 0
    top_ten = 0
    in_set = 0
    not_in_prediction = 0
    num_flights = 0
    check_in_set = False
    for count, flight in enumerate(f):
        # maybe change to a page break later
        file_write.write("\n\n\n\n\n")
        length = len(flight["Partial"])
        file_write.write("#"+ str(count) + ": This flight originated at {Origin} and landed at {Destination}".format(**flight) + " with " + str(length) + " points.\n")
        #destinationAirportDictonary = flight_prediction.overlapping.flight_output(flight["Partial"])
        airportList = flight_prediction.overlapping.multiple_flight_destination_prediction(path, True, False ) # add grid in
        for element, list_count in enumerate(airportList):
            check_in_set = False
            print(type(airportList[list_count][1]))
            for key, key_count in enumerate(airportList[list_count][1]):  
                file_write.write('%s:%s\n' % (key, airportList[list_count][1][key]) + "\n")
                print('%s:%s\n' % (key, airportList[list_count][1][key]) + "\n")
                if ((airportList[list_count][1][key] == flight["Destination"][1:]) and (key_count == 1)):
                    first_prediction += 1
                    check_in_set = True
                if ((airportList[list_count][1][key] == flight["Destination"][1:]) and (1 < key_count <= 3)):
                    top_three += 1
                    check_in_set = True
                if ((airportList[list_count][1][key] == flight["Destination"][1:]) and (3 < key_count <= 10)):
                    top_ten += 1
                    check_in_set = True
                if ((airportList[list_count][1][key] == flight["Destination"][1:]) and (10 < key_count <= len(airportList[list_count][1][key]))):
                    in_set += 1
                    check_in_set = True
            if (check_in_set == False):
                not_in_prediction += 1
            num_flights += 1
            #if(airportList[list_count]):
            #    predictedDest = next(iter(airportList[list_count]))
            #    if(predictedDest == flight["Destination"][1:]):
            #        correct_predictions+=1
    file_write.write("\n\n\n\n\n")
    file_write.write("\nCorrect predictions for the first flight:" + str(first_prediction) + " of " + str(count) + " correct predictions: " +  str((first_prediction/num_flights)*100) + " %% accuracy")
    file_write.write("\nCorrect predictions for the top 3 flight:" + str(top_three) + " of " + str(count) + " correct predictions: " +  str((top_three/num_flights)*100) + " %% accuracy")
    file_write.write("\nCorrect predictions for the top 10 flight:" + str(top_ten) + " of " + str(count) + " correct predictions: " +  str((top_ten/num_flights)*100) + " %% accuracy")
    file_write.write("\nCorrect predictions for the flights in the list:" + str(in_set) + " of " + str(count) + " correct predictions: " +  str((in_set/num_flights)*100) + " %% accuracy")
    file_write.write("\nIncorrect Predictions (for the flights not in the list):" + str(not_in_prediction) + " of " + str(count) + " correct predictions: " +  str((not_in_prediction/num_flights)*100) + " %% accuracy")


    # making so many new lines to differentiate each truncated flight
    file_write.write("\n\n\n\n\n")
    file_write.close()
    return 0

# What to do when the script is called
if __name__ == '__main__':
    sys.exit(main())