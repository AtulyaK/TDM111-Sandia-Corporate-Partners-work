import csv
def overall_csv(path, top_prediction, skipped_predictions, number_of_flights, 
                total_flights_with_prediction, top_three_prediction, top_ten_prediction, top_20_prediction):
    """
    
    Arguments:
        path: path to csv file
        skipped predictions: number of predictions skipped
        number_of_flights: the number of flights gone through
        total_flights_with_predictions: number of flights - skipped predictions
        top_prediction: the top prediction
        top_three_prediction: the top 3 predictions
        top_ten_prediction: the top 10 predictions
        top_20_prediction: the top 20 predictions
    
    Returns:
        None as this just writes to file
    Students:
        Atulya Kadur
    """
    with open(path, "w") as csv_file:
      fields = ['Top What','Correct','# Skipped','Total','Skipped Adjusted Total']
      rows = [['1', top_prediction, skipped_predictions, number_of_flights, total_flights_with_prediction],
              ['3', top_three_prediction, skipped_predictions, number_of_flights, total_flights_with_prediction],
              ['10', top_ten_prediction, skipped_predictions, number_of_flights, total_flights_with_prediction],
              ['20', top_20_prediction, skipped_predictions, number_of_flights, total_flights_with_prediction],
              ]
      writer = csv.writer(csv_file)
      writer.writerow(fields)
      writer.writerows(rows)