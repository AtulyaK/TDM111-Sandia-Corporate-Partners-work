import pandas as pd
import sys
import os.path

"""
This program inputs a dataframe and drops any flights that land outside of North America.

"""

def toNA(input_file, output_file):
    '''Drops flights that land outside of North America

        Students: 
            Ishaan Agrawal
        
        Arguments:
            input: the location of the file of flights to be dropped as a tsv
            ouput: the location of where the new file should be written to
        
        Returns:
          a file of the dataframe with only NA destination airports as a tsv
    '''

    split_tup = os.path.splitext(input_file)
    file_extension = split_tup[1]       #gets file extension
    
    if file_extension == ".tsv":
        separator = '\t'
    elif file_extension == ".csv":
        separator = ","
    
    rawData = pd.read_csv(input_file, sep=separator)

    cleanedFlightData = rawData.dropna(subset = ['LONGITUDE', 'LATITUDE'], how='any')  #drops rows with NaN in Longitude or Latitude 
    dest_index = cleanedFlightData.columns.get_loc('DESTINATION') #gets location of Destination airport column

    dest = cleanedFlightData.iloc[:, dest_index]
    print(f"There are originally {dest.shape[0]} rows in the Destination column. \n")

    rows_with_destination = cleanedFlightData[cleanedFlightData['DESTINATION'].str[0].isin(['C', 'K', 'M'])] #new dataframe only with NA airports in destination
    rows_with_destination = rows_with_destination.reset_index(drop=True)

    dest = rows_with_destination.iloc[:, dest_index]
    print(f"There are now {dest.shape[0]} rows in the Destination column after filtering.")
    output_file = rows_with_destination.to_csv(output_file, index=True) #writes new dataframe to new file


def main():
    if len(sys.argv) != 3:
        print("Usage: script_name.py input_file.tsv output_file.tsv")
        return 1
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    toNA(input_file, output_file)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())