import numpy as np
def confusion_matrix_csv(output_file_name_confusion_matrix, confusion_matrix_dict):
    """makes a CSV confusion matrix and writes to a csv
    Arguments:
        output_file_name_confusion_matrix: the file name for the confusion matrix,
        confusion_matrix_dict: the confusion matrix dictionary of a key being a tuple (actual destination, predicted destination) 
        and the value being the number of occurences
    Returns:
        Nothing as it writes to a csv
    """
    
    all_airports = set()
    for actual, predicted in confusion_matrix_dict.keys():
      all_airports.add(actual)
      all_airports.add(predicted)
    # Convert set to sorted list
    all_airports = sorted(all_airports)
    # Create an empty NumPy array filled with zeros
    array_size = len(all_airports)
    nparray = np.zeros((array_size, array_size), dtype=int)
    airport_to_row = {airport: i for (i, airport) in enumerate(all_airports)}
    for (actual, predicted), count in confusion_matrix_dict.items():
      actual_idx = airport_to_row[actual]
      predicted_idx = airport_to_row[predicted]
      nparray[actual_idx, predicted_idx] = count
    #Write NumPy array to CSV
    nparray = nparray.astype(str)
    header = ['Actual Destination'] + all_airports
    nparray = np.insert(nparray, 0, all_airports, axis=1)
    nparray = np.insert(nparray, 0, header, axis=0)
    np.savetxt(f"{output_file_name_confusion_matrix}", nparray, delimiter=',', fmt='%s')