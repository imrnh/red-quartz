def separate_datetime_object_in_db(theObj):
    theObj = "2022-07-23T17:14:26.160754" #Example obj
    (date_, time_) = (str(theObj)).split('T')
    (year, month, day) = list(map(int, date_.split("-")))
    #(hour, minute, sec) = list(map(int, time_.split(":")))

    return {
        "year": year,
        "month": month,
        "day": day,
    }
