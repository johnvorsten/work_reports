# -*- coding: utf-8 -*-
"""
Created on 2022-5-22

A Point Definition report is a structured text file representing objects with
common fields for each object.
This script will aggregate parse structured text and arrange data in a comma separated value
list of objects and its associated attributes.

Structured text attributes:
[Point System Name, Point Name, Point Type, Supervised, Revision Number, 
Classification, Descriptor, Panel Name, Point Address, Text Table, 
Initial Value, Totalization, Enabled for RENO, Alarm Issue Management, 
Graphic Name, Informational Text, Alarm Type, Alarm Count 2, Normal ack Enabled, 
Print Info with Alarm, Mode Point, Mode Delay (min.), Default Destination 1, 
Default Destination 2, Default Destination 3, Default Destination 4, Alarm Mode]

The primary key used to differentiate objects is the 'Point System Name' attribute. All
other attributes are non-unique

@author: John Vorsten
"""
# %%
# Python imports
import re
from dataclasses import dataclass, make_dataclass, asdict, fields
from xml.sax.xmlreader import AttributesNSImpl
from typing import List
from io import TextIOBase, TextIOWrapper
import csv

# Third party imports
import pandas as pd

# Local imports

# Declarations
ATTRIBUTES = ["Point System Name", "Point Name", "Point Type", "Supervised", "Revision Number",
              "Classification", "Descriptor", "Panel Name", "Point Address",
              "Slope", "COV Limit", "Engineering Units", "Analog Representation",
              "Text Table",
              "Initial Value", "Totalization", "Enabled for RENO", "Alarm Issue Management",
              "Graphic Name", "Informational Text", "Alarm Type", "Alarm Count 2", "Normal ack Enabled",
              "Print Info with Alarm", "Mode Point", "Mode Delay \(min\.\)", "Default Destination 1",
              "Default Destination 2", "Default Destination 3", "Default Destination 4", "Alarm Mode"]
# Note MOde Delay (min.) is different
ATTRIBUTES_FIELDS = ["point_system_name", "point_name", "point_type", "supervised", "revision_number",
                     "classification", "descriptor", "panel_name", "point_address",
                     "slope", "cov_limit", "engineering_units", "analog_representation",
                     "text_table",
                     "initial_value", "totalization", "enabled_for_reno", "alarm_issue_management",
                     "graphic_name", "informational_text", "alarm_type", "alarm_count_2", "normal_ack_enabled",
                     "print_info_with_alarm", "mode_point", "mode_delay_min", "default_destination_1",
                     "default_destination_2", "default_destination_3", "default_destination_4", "alarm_mode"]
# Matches start of line with any valid word character
# including letter, number, underscore
regex_start_with_valid_character = re.compile("^\w")
# Dynamically create and compile regex based on ATTRIBUTES
# These will be used to parse text line by line
regex_searches = []
for attribute_name in ATTRIBUTES:
    reg = re.compile(attribute_name)
    regex_searches.append(reg)

class ProgrammerError(Exception):
    pass

# %%

@dataclass
class PointDefinition:
    point_system_name: str
    point_name: str = ''
    point_type: str = ''
    supervised: str = ''
    revision_number: str = ''
    classification: str = ''
    descriptor: str = ''
    panel_name: str = ''
    point_address: str = ''
    slope: str = ''
    cov_limit: str = ''
    engineering_units: str = ''
    analog_representation: str = ''
    text_table: str = ''
    initial_value: str = ''
    totalization: str = ''
    enabled_for_reno: str = ''
    alarm_issue_management: str = ''
    graphic_name: str = ''
    informational_text: str = ''
    alarm_type: str = ''
    alarm_count_2: str = ''
    normal_ack_enabled: str = ''
    print_info_with_alarm: str = ''
    mode_point: str = ''
    mode_delay_min: str = ''
    default_destination_1: str = ''
    default_destination_2: str = ''
    default_destination_3: str = ''
    default_destination_4: str = ''
    alarm_mode: str = ''

def _trim_and_strip_text(regex_match: re.Match, line: str) -> str:
    """Given a matched regex Match object and a line,
    strip the raw text of blank spaces, and return the value
    Example:
    Raw line:
    'Point System Name:       B01.4307.FR7.STAEFA.COMFAIL'
    Regex match object contains a match starting at character 0
    and ending at character 18
    Return B01.4307.FR7.STAEFA.COMFAIL
    """
    field_pos = regex_match.end()
    field_name = line[field_pos:-1]  # Return string
    field_name = field_name.strip(": ")  # Clean string of spaces

    return field_name


def _find_file_primary_key_start_lines(filepath: str) -> List[int]:

    primary_key_offsets = []  # List of byte offsets
    offset: int = 0  # Byte offset location
    regex: re.Pattern = regex_searches[0]
    line: str = ''

    with open(filepath, 'rt') as file:
        # Find end of file...
        file.seek(0, 2)  # End of strem
        end_location: int = file.tell()
        file.seek(0, 0)  # start of stream

        while file.readable():

            # Current offset will be beginning of next line
            # TODO Return the current stream position as an opaque number.
            # The number does not usually represent a number of bytes in the underlying binary storage.
            # Does this mean tell() is not reliable to tell the current offset?
            current_byte_offset = file.tell()
            line = file.readline()

            # First, search the line for text matching the primary key which is
            # 'Point System Name:'
            # If we find a line containing a primary key then record the file offset
            point_result = regex_searches[0].search(line)
            if point_result:
                primary_key_offsets.append(current_byte_offset)

            # EOF occurs with blank string and no more bytes to read
            if line == '' and file.tell() == end_location:
                break

    return primary_key_offsets

def _parse_text_from_offset_to_offset(file: TextIOWrapper, start: int, stop: int) -> PointDefinition:

    # Seek to start byte
    file.seek(start)

    # Instantiate to test if we failed to parse
    point: PointDefinition = None

    while file.readable():
        # Manually iterate through lines
        line = file.readline()

        # First, search the line for text matching the primary key which is
        # 'Point System Name:'
        # If we find a line containing a primary key then attempt to create a new
        # PointDefinition object
        point_result = regex_searches[0].search(line)

        # Each regex match object has useful attributes and methods
        # re.match.end() : (int) position of end of string matched by match object
        if point_result:
            field_name = _trim_and_strip_text(point_result, line)
            # Create a PointDefinition instance and append to list
            point = PointDefinition(point_system_name=field_name)

            # Continue to parse using the rest of the regex searches available
            # If we exhaust our list of regex searches then we exit the for
            # Loop and continue reading lines
            line = file.readline()

            # If the next line does not start with a word character, then skip it
            while not regex_start_with_valid_character.search(line):
                line = file.readline()

            # Do not use the first regex search, which is the primary key regex
            # Looking for 'Point System Name:'
            idx: int = 1
            while idx < len(regex_searches):
                match = regex_searches[idx].search(line)
                if match:
                    # Update the field for the current dataclass object
                    field_name = _trim_and_strip_text(match, line)
                    key = ATTRIBUTES_FIELDS[idx]
                    point.__setattr__(key, field_name)
                    # Match is found, so continue searching the file
                    line = file.readline()
                    # Keep track of the last successful search index
                    successful_index = idx
                    idx += 1
                elif all((not regex_start_with_valid_character.search(line), file.tell() < stop)):
                    # Iterate until we find a valid line
                    while (not regex_start_with_valid_character.search(line)):
                        line = file.readline()
                else:
                    # No match is found, so continue trying other regex
                    idx += 1

        if file.tell() >= stop:
            break

    if point:
        return point
    
    raise ProgrammerError("whoopsies: ", str(point))

def parse_text_to_list(filepath: str) -> List[PointDefinition]:
    """Using the pre-parsed offsets, iterate through text file"""

    points_list: List[PointDefinition] = []
    offsets: List[int] = _find_file_primary_key_start_lines(filepath)
    current_offset_index: int = 0
    start: int
    stop: int

    with open(filepath, 'rt') as file:

        for current_offset_index in range (0, len(offsets) - 1):
            start: int = offsets[current_offset_index]
            stop: int = offsets[current_offset_index+1]
            point = _parse_text_from_offset_to_offset(file, start, stop)
            points_list.append(point)

    return points_list

def write_dataclass_to_csv(filepath: str, points: List[PointDefinition]) -> None:

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

# %%
