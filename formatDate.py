def formatDate(date):
    date = date.replace('Z', '2')
    date = date.replace('O', '0')
    new_date = ""
    for c in date:
        if c.isdigit():
            new_date += c
            
    return new_date