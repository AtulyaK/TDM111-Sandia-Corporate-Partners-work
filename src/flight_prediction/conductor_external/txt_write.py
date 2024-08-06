def setup(path):
    """writes the initial line to the file

    Arguments:
        file path

    Returns:
         None
    """
    with open(path,"a") as file:
      file.write("Output of the data:")
      
def destination_write(path,destination,percent):
    """writes the actual destination for each flight to a file

    Arguments:
        path of file to write to, the destination, and the 
        percentage of the flight not truncated (remaining)

    Returns:
         None
    """
    with open(path,"a") as file:
        file.write("\n\n\n\n\n")
        file.write(f"Destination: {destination} \nPercentage: = {percent}\n")
        
def destination_predicted(path,counter,predicted_destination):
    """writes the top 20 predicted destinations for each flight to a file

    Arguments:
        path of file to write to,desination 
    Returns:
         None
    """
    with open(path,"a") as file:
        file.write(f"Predicted Destination {counter}: {predicted_destination}\n")

def overall_txt_output(path, x_prediction, top_x_prediction, number_of_flights, skipped_predictions):
    """writes the overall values to the file. 
    
    Arguments:
        path to write to, 
        the prediction top x (1,3,10,20),
        the number corresponding to the top x prediction,
        number of flights,
        number of skipped predictions,
        
    Returns:
        None as it writes to a file    
    
    """
    with open(path,"a") as file:
        if x_prediction == 1:
            file.write("First Prediction:\n")
        elif x_prediction == 3:
            file.write("Top Three Prediction:\n")
        elif x_prediction == 10:
            file.write("Top Ten Prediction:\n")
        elif x_prediction == 20:
            file.write("Top Twenty Prediction:\n")
        elif x_prediction == "Overall":
            file.write("Overall Prediction:\n")
        file.write(f"{top_x_prediction} of {number_of_flights} correct predictions:"
        f" {(top_x_prediction / number_of_flights) * 100:.2f}% accuracy\n")
        file.write(f"{skipped_predictions} of {number_of_flights} skipped predictions:"
        f" {(skipped_predictions / number_of_flights) * 100:.2f}% skipped predictions\n")
        file.write(f"{number_of_flights - skipped_predictions} of {number_of_flights} predictions made:"
        f" {((number_of_flights - skipped_predictions) / number_of_flights) * 100:.2f}% predictions made\n")
        total_flights_with_prediction = number_of_flights - skipped_predictions
        file.write(f"{top_x_prediction} of {total_flights_with_prediction} correct predictions:"
        f" {(top_x_prediction / total_flights_with_prediction) * 100:.2f}% accuracy\n")
    

 
