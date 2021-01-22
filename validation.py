"""
Name
    validation

DESCRIPTION
    This module contains functions for validating the user input

CLASS
    None

FUNCTION
   is_valid_number             -- returns true if text is positive integer
   is_valid_number_or_blank    -- returns true if text is positive integer or blank
   is_valid_day                -- returns true if day value is valid for the selected month
   is_valid_date               -- returns true if date value is a valid date (mm/dd/yy format)

DATA
    text                       -- contains the user input in string format
"""

import re


# validate text entered is a non-negative integer
def is_valid_number(text):

    is_valid = True
    try:
        value = int(text)
        if value < 0:
            raise ValueError
    except ValueError:
        is_valid = False
    return is_valid


# validate text entered is a non-negative integer or blank
def is_valid_number_or_blank(text):
    is_valid = True
    if text != "":
        is_valid = is_valid_number(text)
    return is_valid


# validate the day selected based on the month selected
def is_valid_day(month, day):
    is_valid = True
    if int(month) in [2,4,6,9,11]: # Feb, April, June, Sept, Nov
        if int(month) == 2:    # February
            if int(day) > 28:  # no leap year logic at this time, sorry!
                is_valid = False
        else:
            if int(day) > 30:
                is_valid = False
    else:
        if int(day) > 31:
            is_valid = False
    return is_valid


# validate a date in the format mm/dd/yy was entered
def is_valid_date(text):
    is_valid = True
    if text != "":
        date_match = re.match('^[0-9][0-9][/](.*)[0-9][0-9][/](.*)[0-9][0-9]$', text)
        if date_match is not None:
            extract_date = re.split('[/]', text)
            month = extract_date[0]
            if int(month) > 12:
                is_valid = False
            else:
                day = extract_date[1]
                is_valid = is_valid_day(month, day)
        else:
            is_valid = False
    return is_valid
