import tracktable
from tracktable.core.geomath import distance


# 100 Test Count
# 63% - Linear Sum
# 78% - Second Half Data - Linear Sum
# 83% - Forward Weighted Sum
# 78% - Second Half Data - Forward Weighted Sum
# 39% - Backward Weighted Sum
# 53% - Step 5 Sum

# 400 Test Count
# 65.25% - Linear Sum
# 87.75% - Forward Weighted Sum

def constant_weighting(destinationAirport, curve_function=lambda x: x):
    destinationAirportDictionary = {}

    for key, value in destinationAirport.items():
        destinationAirportDictionary[key] = destinationAirportDictionary.get(key, 0) + curve_function(value)
    return destinationAirportDictionary


def weighting_func(destinationAirport, flight, point_number, curve_function=lambda x: x, x_axis="index"):
    """Finds the dictionary for the latitude and longitude provided.

    Arguments:
        destinationAirport: prediction in a dict from a flight generated from flight_destination_prediction()
        flight: Tracktable trajectory of a truncated flight
        point_number: What number a point is in a flight
        curve_function: A lambda function with a x axis parameter for the weighting function to be implemented
        x_axis: A string of one of the following values: 'index', 'distance', 'time'

    Returns:
        Dictionary of Destination Airports 
    """
    
    if x_axis == "index":
        divisor = len(flight)
    elif x_axis == "distance":
        divisor = distance(flight[0], flight[-1])
    elif x_axis == "time":
        divisor = (flight[0].timestamp - flight[-1].timestamp).total_seconds()

    if x_axis == "index":
        # Sets the x as index
        x = point_number / divisor
    elif x_axis == "distance":
        # Sets the x as distance between current position and starting position
        x = distance(flight[0], flight[point_number]) / divisor
    elif x_axis == "time":
        # Sets the x as time difference between current position and starting position
        x = (flight[point_number].timestamp - flight[0].timestamp).total_seconds() / divisor

    destinationAirportDictionary = {}

    for key, value in destinationAirport.items():
        destinationAirportDictionary[key] = destinationAirportDictionary.get(key, 0) + value * curve_function(x)
    return destinationAirportDictionary
