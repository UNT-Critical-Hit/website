import sys

def parse_data(data):
    officers = []

    lines = data.split('\n')
    officer = {}
    for line in lines:
        if not line:
            officers.append(officer)
            officer = {}
        else:
            line = line.split(': ')
            officer[line[0].lower().replace(' ','_')] = line[1]
    officers.append(officer) # append the final officer

    return officers