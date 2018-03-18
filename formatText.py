replacementsDate = {'Z': '2', 'O': '0', '(]': '0',
                    'JAN': '01', 'FEB': '02', 'MAR': '03',
                    'APR': '04', 'MAY': '05', 'JUNE': '06',
                    'JULY': '07', 'AUG': '08', 'SEP': '09',
                    'OCT': '10', 'NOV': '11', 'DEC': '12',
                    'JUN': '06', 'JUL': '07'}
replacementsLot = {')(': 'X', ' ': ''}

def formatDate(date):
    for key, value in replacementsDate.items():
        date = date.replace(key, value)
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
        return ""
        
def formatLot(lot):
    for key, value in replacementsLot.items():
        lot = lot.replace(key, value)
    if lot.lower().startswith('lot '):
        return lot[4:]
    elif lot.lower().startswith('lot'):
        return lot[3:]
    elif lot.lower().startswith('(10)'):
        return lot[4:]
    elif len(lot) == 7 and lot.isalnum():
        return lot
    else:
        return ""