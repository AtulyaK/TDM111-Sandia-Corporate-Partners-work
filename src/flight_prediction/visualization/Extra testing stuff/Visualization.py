import tracktable
import pandas as pd
import os.path




from tracktable.core import geomath
from tracktable.domain.terrestrial import TrajectoryPointReader
from tracktable.applications.assemble_trajectories import AssembleTrajectoryFromPoints
from tracktable.render.render_trajectories import render_trajectories

from datetime import datetime, timedelta


print(tracktable.__version__)
print("All libraries imported!")

data_filename = ("/anvil/projects/tdm/corporate/sandia-trajectory/previous_files/flight/data/raw_data/oneDay.tsv")
inFile = open(data_filename, 'r')
reader = TrajectoryPointReader()
reader.input = inFile
reader.comment_character = "#"	#What character is used for comments
reader.field_delimiter = "\t"	#What character "breaks" each data value ex: Comma-Separated Values


#Columns start at 0, ex: 0 is column A, 2 is column C
reader.object_id_column = 0 	#What column holds the object ID
reader.timestamp_column = 1 	#What column holds the timestamp
reader.coordinates[1] = 3		#What column holds LAT data
reader.coordinates[0] = 2		#What column holds LONG data
reader.set_real_field_column('speed', 4) #Extra data (heading)
reader.set_real_field_column('heading', 5) #Extra data (heading)
reader.set_real_field_column('altitude', 6) #Extra data (altitude)
reader.set_string_field_column('ac_type', 7)
reader.set_string_field_column('departure', 8) #Dearture Airport
reader.set_string_field_column("destination", 9) #Destination Airport

#Combine datapoints together using the object_id
builder = AssembleTrajectoryFromPoints()
builder.input = reader
builder.minimum_length = 1
builder.separation_time = timedelta(minutes=30)
traj = list(builder.trajectories())


flightOfInterest = traj[300]



flightLength = tracktable.core.geomath.length(flightOfInterest)

convexHullRatio = tracktable.core.geomath.convex_hull_aspect_ratio(flightOfInterest)



departures = []
destinations = []
for flight in traj:
    departures.append(flight[0].properties['departure'])
    destinations.append(flight[0].properties['destination'])
    # for point in flight:
    #     departures.append(point.properties["departure"])
    #     destinations.append(point.properties["destination"])
depDF = pd.DataFrame(departures)
destDF = pd.DataFrame(destinations)

print(depDF.head())

def visualize(listOfTrajectories):

    
    possible_colors = [0.1, 0.5, 0.5, 1.0, 1.0]
    colors = []
    if len(listOfTrajectories) > 5:
        
        colors = possible_colors
        for i in range(5, len(listOfTrajectories) - 1):
            colors.append(1.2)
    
    if len(listOfTrajectories) == 5:
        colors = possible_colors
    else:
        for i in range(len(listOfTrajectories)):
            colors.append(possible_colors[i])
    return colors
test_list = [traj[3000], traj[2001], traj[708], traj[405], traj[1], traj[98]]        
tracktable.render.render_trajectories.render_trajectories(test_list, backend='', simplify_traj=False, simplify_tol=0.0001, gradient_hue = visualize(test_list) save=True)

    
            
