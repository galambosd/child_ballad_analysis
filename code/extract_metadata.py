# make a dictionary mapping ballad number to metadata
# make new columns like so
# df['date'] = date_dict[df.num]
import re
from sys import argv
import pprint as pp
import pandas as pd


def findFirst(compiled_re, input, error_term = None):
    list = compiled_re.findall(input)
    if not list:
        return error_term
    else:
        return list[0]

# we have all ballads with ID info and refrain
# create a dataframe with all that info (which we have)

# given an input string and a regular expression
# find the dates and origins associated with each name
def extractMetadata(input, search_term):
    search_re = re.compile(search_term)
    name_re = re.compile(r'\ANAME:[^\n]+\nDESCRIPTION')
    date_re = re.compile(r'EARLIEST_DATE: [^\d]*(\d{4})')
    origin_regex = r'FOUND_IN: ([^\n;]+)'
    to_replace_re = re.compile(r'\([^ ]+\)')
    origin_re = re.compile(origin_regex)
    ballad_re = re.compile(r'===\n([^=]+)\n')
    ballads = ballad_re.findall(input)
    dateDict = {}
    originDict = {}
    for ballad in ballads:
        # find the name
        # name = findFirst(name_re, input)
        name_list = name_re.findall(ballad)
        if not name_list:
            continue
        name = name_list[0]
        # check if the name contains the term
        number_list = search_re.findall(name)
        if not number_list:
            continue
        number = number_list[0]
        if len(number) >= 1:
            # grab the date and origin
            date = findFirst(date_re, ballad)
            origin = findFirst(origin_re, ballad)
            if origin != None:
                origin = to_replace_re.sub('', origin)
                origin = origin.split(' ')
            # add it to dictionary
            dateDict[number] = date
            originDict[number] = origin
    # return a dictionary of number --> date
    # and number --> origin
    return dateDict, originDict


def test_extract_metadata():
    file_name = argv[1]
    file = open(file_name)
    input = file.read()
    file.close()
    target_name = r'\[Child (\d+)\]'
    dates, origins = extractMetadata(input, target_name)
    pp.pprint(dates)
    print(set(dates.values()))
    origin_list = []
    for origin in origins.values():
        if origin == None:
            continue
        origin_list += origin
    pp.pprint(origins)
    print(set(origin_list))


if __name__ == '__main__':
    test_extract_metadata()
