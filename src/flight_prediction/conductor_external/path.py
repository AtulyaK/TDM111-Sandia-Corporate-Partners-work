import time
def timestamp_to_string(when, txt, csv):
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