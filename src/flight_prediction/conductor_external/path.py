import time
def timestamp_to_string(when, txt, csv):
    """_summary_

    Args:
        when (time): time of starting the conductor program
        txt (boolean): whether or not to generate the text file
        csv (boolean): whether or not to generate the csv file

    Returns:
        string: file name or location of both files.
    Students:
        Atulya Kadur
    """
    if txt == True and csv == False:
        date = f"{when.year}-{when.month}-{when.day}"
        time = f"{when.hour}-{when.minute}-{when.second}-{when.microsecond}"
        return f"{date}_{time}.txt"
    if csv == True and txt == False:
        date = f"{when.year}-{when.month}-{when.day}"
        time = f"{when.hour}-{when.minute}-{when.second}-{when.microsecond}"
        return f"{date}_{time}.txt"
    if txt == False and csv == False:
        date = f"{when.year}-{when.month}-{when.day}"
        time = f"{when.hour}-{when.minute}-{when.second}-{when.microsecond}"
        return f"{date}_{time}_visualization/"