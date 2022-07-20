#String format: " YYYY-MM-DD  HOUR:MIN  DAY_OF_WEEK "

def repeatOnDecoder_getDate(workingString): #This "workingString" will always be a list if we directly pass the retrived data of the column from the database.
    listOfObjects = [] 
    for itr in workingString:
        
        #Splitting the main string into date time and day_of_week
        date, time, day_of_week = itr.split(" ") 
        
        #Splitting the date and time substring.
        year, month, date = date.split("-")
        hour, min = time.split(":")

        obj = {
            "year": year,
            "month": month,
            "date": date, 
            "hour": hour,
            "minute": min,
            "day_of_week": day_of_week
        }
        listOfObjects.append(obj)

    return listOfObjects #The output of the function is also list which contains multiple dictionaries.