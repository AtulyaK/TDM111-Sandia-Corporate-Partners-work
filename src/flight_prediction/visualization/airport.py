import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from tracktable.info.airports import airport_information

# module use /anvil/projects/tdm/opt/core
# module load tdm
# module load python/sandia

"""This function makes a color list for the airport map based on the number of airport codes

  Args:
    a: num of airport codes

  Returns:
    returns the updated list of colors based on the number. 
  """

def get_list_of_colors(num_of_airports):
  possible_colors = ['green', 'blue', 'blue', 'orange', 'orange']
  colors = []
  if num_of_airports > 5:
      colors = possible_colors
      for i in range(5, num_of_airports ):
          colors.append('red')
  
  if num_of_airports == 5:
      colors = possible_colors
  else:
      for i in range(num_of_airports):
          colors.append(possible_colors[i])
  return colors
test_list = ['STL', 'MCI', 'ORD', 'LAX']

"""This function puts circles on the map of locations of airports passed into it.

  Args:
    a: List of airport codes
    b: File name for output picture.

  Returns:
    N/A draws the picture and outputs it to same directory that program is in.
  """
def draw_airports(airport_codes, origin, file_name):

    airport_list = []
    origin_code = origin #Last code in the list is origin
    count = 1
    initial_size = 1
    decrease_factor = 1
    for counter,airport in enumerate(airport_codes):
        if counter < 20:
          temp =[]
          tempport = airport_information(airport)
          try:
            latitude, longitude, elevation = tempport.position
            temp = [f'Airport {count}', tempport.city, longitude, latitude]
            airport_list.append(temp)
          except AttributeError:
            print("error with NONE TYPE OBJECT")
    origin = []
    originport = airport_information(origin_code)
    origin_lat, origin_long, origin_elev = originport.position
    origin = [f'Origin Airport', originport.city, origin_long, origin_lat]
    airport_list.append(origin)
    df = pd.DataFrame(airport_list, columns=['Name', 'City', 'Latitude', 'Longitude'])
    
    # Create DataFrame and GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    fig, ax = plt.subplots(figsize=(15, 10))
    world.plot(ax=ax, color='lightgrey')


    ax.set_xlim(-125, -66)  
    ax.set_ylim(24, 49)


    # Plot the origin airport with a unique color and size
    origin_point = gdf[gdf['Name'] == 'Origin Airport'].iloc[0]
    plt.plot(origin_point['Longitude'], origin_point['Latitude'], marker='o', color='pink', markersize=10)
    plt.text(origin_point['Longitude'], origin_point['Latitude'], ' ' + origin_point['City'] + ' (Origin)', fontsize=9, ha='left', va='center')

    # Plot other airports, store their points and draw lines from origin to them
    marker_size = max(len(airport_codes), 10)
    colors = get_list_of_colors(len(airport_codes))
    color_count = 0
    for _, row in gdf[gdf['Name'] != 'Origin Airport'].iterrows():
        plt.plot(row['Longitude'], row['Latitude'], marker='o', color=colors[color_count], markersize=marker_size)
        plt.text(row['Longitude'], row['Latitude'], ' ' + row['City'], fontsize=9, ha='left', va='center')
        # Draw lines from origin to each airport
        plt.plot([origin_point['Longitude'], row['Longitude']], [origin_point['Latitude'], row['Latitude']], color=colors[color_count], linestyle='--', linewidth=1)
        color_count += 1
        marker_size -= 1

    plt.savefig(f'{file_name}.png', dpi=300)
    plt.show()
#End of function