# -*- coding: utf-8 -*-
"""
Created on 2022-5-22

A Point Log report is a structured text file representing objects with
common fields for each object.
This script will aggregate parse structured text and arrange data in a comma separated value
list of objects and its associated attributes.

Structured text attributes include ['Name:Suffix','Address','Description','Value/State',
'Status','Priority']

The primary key used to differentiate objects is the 'Name:Suffix' attribute. All
other attributes are non-unique

Example report:
4/27/2022                            Someone                            04:34 PM
                            Panel Point Log Report ( Temporary Report ) 
 
Selected Points:  B01.4307.FR7.STAEFA.COMFAIL, B01.4307.RF5.STAEFA.COMFAIL, ...
(863 Points)
Selected Panels:  B03.4331a.MBC01
Filter:  All Points
 
Name:Suffix                   Address         Description        Value/State       Status  Priority
________________________________________________________________________________
B01.4307.FR7.STAEFA.COMFAIL   -Virtual-       (CRITALM COMFAIL ) NORMAL             -N-       NONE 
****************************************************************************************************
B01.4307.RF5.STAEFA.COMFAIL   -Virtual-       (CRITALM COMFAIL ) NORMAL             -N-       NONE 
****************************************************************************************************
B01.4325.RF6.STAEFA.COMFAIL   -Virtual-       (CRITALM COMFAIL ) NORMAL             -N-       NONE 
****************************************************************************************************
B01.4357.AHE1.DDC01.ADD       3 06 01         (                ) 1038.00            -N-       NONE 
****************************************************************************************************
B01.4357.AHE1.DDC01.APP       3 06 02         (                ) 6095.00            -N-       NONE 
****************************************************************************************************
B01.4357.AHE1.DDC01.COMF      3 06 99         (                ) ON                 -N-       NONE 
****************************************************************************************************

                                     - 1 -
Name:Suffix                   Address         Description        Value/State       Status  Priority
________________________________________________________________________________
B01.4750.DD01:AUX CLG VEL     1 05 53         (                ) 611.98      CFM    -N-       NONE 


Important qualities of this structured text
1. The spacing between data attributes is not fixed. The spacing is determined by the data and 
computer which generate the report
2. Asterisks always follow an object
3. Data attributes always start at the same position as the header, and is continuous through the report
4. White space characters are unicode space U+0020
5. Files are encoded UTF-8
6. Lists of points always start with a header (parser starts when header line encountered)
7. Lists of points always end with a line of asterisks followed by a blank line

@author: John Vorsten
"""
# %%
# Python imports
import re
from dataclasses import dataclass, fields, asdict
from typing import List, Dict
from io import TextIOBase, TextIOWrapper
import csv

# Third party imports

# Local imports

# Declarations
HEADERS = ['Name:Suffix','Address','Description','Value/State','Status','Priority']
# Note MOde Delay (min.) is different
ATTRIBUTES_FIELDS = ['name','address','description','value','status','priority']
# Character position of start of each element of HEADERS within the report header line
HEADERS_START: Dict[str, int] = {}
for header in HEADERS:
    HEADERS_START[header] = 0

# Matches start of line with any valid word character
# including letter, number, underscore
regex_start_with_valid_character = re.compile("^\w[^_]{2}")

class ProgrammerError(Exception):
    pass

# Hold parsed line data
@dataclass
class PointDefinition:
    name: str
    address: str
    description: str
    value: str
    status: str
    priority: str

#%%

def _trim_and_strip_text(line: str, start: int, end: int) -> str:
    """Given a start index, end, and a line,
    strip the raw text of blank spaces, and return the value
    Example:
    Raw line:
    '       B01.4307.FR7.STAEFA.COMFAIL       \n'
    Return B01.4307.FR7.STAEFA.COMFAIL
    """
    field_name = line[start:end]  # Return string
    field_name = field_name.strip(": \n")  # Clean string of spaces

    return field_name

def _determine_header_start_positions(line: str) -> None:
    """The header of this type of text file contains the character keys 
    ['Name:Suffix', 'Address','Description','Value/State','Status','Priority']
    with spaces in-between keys. The number of white-spaces between keys is dependent
    on data defined within the file, and cannot be explicitly known.
    Return the character start position of each key within a header file"""

    for header in HEADERS:
        if header in line:
            HEADERS_START[header] = line.find(header, 0, None)
        else:
            raise ProgrammerError(f'{header} was expected within the header line {line}, but it was not found')

    return None

def _line_is_header(line: str) -> bool:
    """Determine if a line is a header. Headers always contain the values
    ['Name:Suffix', 'Address','Description','Value/State','Status','Priority']"""

    for header in HEADERS:
        if header in line:
            pass
        else:
            return False

    return True

def _line_is_list_end(line: str, previous_line: str) -> bool:
    """Determine if a line is the end of a list of points. 
    Lists of points always end with a line of asterisks followed by a blank line
    or end of line character"""
    is_asterisk = _line_is_asterisk(previous_line)
    is_blank = any((line == '', line == '\n'))
    if all((is_asterisk, is_blank)):
        return True

    return False

def _line_is_asterisk(line: str) -> bool:
    """Determine if a line is a series of asterisk characters"""

    asterisk_line = '**********************************'
    if asterisk_line in line:
        return True

    return False

def _parse_object_line(line: str, headers_start: Dict[str, int]) -> PointDefinition:
    """Parse data attributes from a line. Data attributes start at the exact
    same position as their header"""

    name: str = _trim_and_strip_text(line, headers_start['Name:Suffix'], headers_start['Address'])
    address: str = _trim_and_strip_text(line, headers_start['Address'], headers_start['Description'])
    description: str = _trim_and_strip_text(line, headers_start['Description'], headers_start['Value/State'])
    value: str = _trim_and_strip_text(line, headers_start['Value/State'], headers_start['Status'])
    status: str = _trim_and_strip_text(line, headers_start['Status'], headers_start['Priority'])
    priority: str = _trim_and_strip_text(line, headers_start['Priority'], -1)

    point = PointDefinition(name, address, description, value, status, priority)

    return point

def parse_text_to_pointdefinition_list(filepath: str) -> List[PointDefinition]:
    """Iterate through a text file and parse good lines to a list of PointDefinition objects
    See rules about how to determine which line is good"""

    points_list: List[PointDefinition] = []
    # First, find the first header line to populate data start positions
    with open(filepath, 'rt', encoding='UTF-8') as file:
        # Find end of file...
        file.seek(0, 2)  # End of strem
        end_location: int = file.tell()
        file.seek(0, 0)  # start of stream

        for line in file:

            if _line_is_header(line):
                _determine_header_start_positions(line)
                break

            if line == '' and file.tell() == end_location:
                # Header line not found
                raise ValueError(f"Header line not found in file. A header containing values {HEADERS} is required")

    # Then, parse the text file
    with open(filepath, 'rt', encoding='UTF-8') as file:
        # Find end of file...
        file.seek(0, 2)  # End of strem
        end_location: int = file.tell()
        file.seek(0, 0)  # start of stream
        # True if within object list area
        in_list_area = False
        previous_line: str = ''

        for line in file:
            if not regex_start_with_valid_character.search(line):
                if in_list_area and _line_is_list_end(line, previous_line):
                    in_list_area = False
                previous_line = line
                continue
            elif _line_is_header(line):
                in_list_area = True
                previous_line = line
            elif _line_is_asterisk(line):
                previous_line = line
                continue
            elif in_list_area:
                # Lines are valid, not an asterisk line, not a header, and in list area
                point = _parse_object_line(line, HEADERS_START)
                points_list.append(point)
                previous_line = line

    return points_list

def write_dataclass_to_csv(filepath: str, points: List[PointDefinition]) -> None:
    """"""

    # Get collection of keys from the PointDefinition dataclass for writing the header
    keys: list = []
    for field in fields(PointDefinition):
        keys.append(field.name) # Name of field

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(keys)
        # Iterate through each points object and write
        for point in points:
            values = list(asdict(point).values())
            writer.writerow(values)

    return None
