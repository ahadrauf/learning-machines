def formatDate(date):
    date = date.replace('Z', '2')
    date = date.replace('O', '0')
    date = date.replace("JAN", '01')
    date = date.replace("FEB", '02')
    date = date.replace("MAR", '03')
    date = date.replace("APR", '04')
    date = date.replace("MAY", '05')
    date = date.replace("JUNE", '06')
    date = date.replace("JULY", '07')
    date = date.replace("AUG", '08')
    date = date.replace("SEP", '09')
    date = date.replace("OCT", '10')
    date = date.replace("NOV", '11')
    date = date.replace("DEC", '12')
    new_date = ""
    for c in date:
        if c.isdigit():
            new_date += c
    
    if len(new_date) == 8: #month, day, year
        if new_date[0] == '2':
            return new_date[0:4] + '-' + new_date[4:6] + '-' + new_date[6:8]
        else:
            return new_date[4:8] + '-' + new_date[0:2] + '-' + new_date[2:4]
    elif len(new_date) == 6: #month, year
        if new_date[0] == '2':
            return new_date[0:4] + '-' + new_date[4:6]
        else:
            return new_date[2:6] + '-' + new_date[0:2]
    else:
        return new_date