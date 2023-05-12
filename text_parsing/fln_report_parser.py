# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:34:54 2019

The text file report from commissioning tool has the following nested format:
The report name is "system profile report" and export the report as a text file

# Example
{
    'downtown alberta JP morgan chase building': { # Jobsite name
        'Main building network':{ # Building level network name
            'CP1.20342.33':{ # Field panel name
                'Field level network #2134':{ # Field level network name
                    'FJDSO.43255.32:{ # Device name
                        'application':1, # Application number
                        'drop':234, # Drop number
                    }
                }
            }
        }
    }
}


@author: jvorsten
"""
# Python imports
import re
from typing import Dict, Tuple, List
import csv

# Third party imports
# import pandas as pd

# Local imports

# Declarations
BLN_DICT = Dict[
    str,Dict[ # 'Job Site':{
        str,Dict[ # 'Field Panel':{
            str,Dict[ # 'FLN':{
                str,Dict[ # 'FLN Device':{
                    str,Dict[str,int] # {}'Application:int,'Drop':int}
                ]
            ]
        ]
    ]
]

# %%

def create_bln_dict(file_path: str):
    """Outputs a dictionary structure after iterating through all lines in an
    input text file. The output dict represents the network FLN structure
    of the text file. The text file is the "system profile" report
    in commissioning tool
    inputs
    -------
    file_path : (str) .txt file of 'system profile' report from commissioning tool
    outputs
    -------
    bln_dict : (dict) representing structured network hierarchy
    bln_dict = {
        'Job Site:':
            {'BLN':
                {'Field Panel:':
                    {'FLN:':
                        {'FLN Device:':
                            {'Application':0, 'Drop':1}}}}}}
    """

    reg_job = re.compile('Job Site:')
    reg_bln = re.compile('BLN:')

    reg_field = re.compile('Field Panel:')
    reg_instance = re.compile('Device Instance:')
    reg_fln = re.compile('FLN:') # Field level network name
    reg_device = re.compile('FLN Device:') # Device name
    reg_app = re.compile('Application:') # device application number
    reg_drop = re.compile('Drop:') # Device drop
    reg_space = re.compile(': ') # space... not used for anything

    # result = regex.match(string)
    bln_dict:BLN_DICT = {}

    with open(file_path, 'r') as f:
        for line in f:

            # Each regex pattern search result returns a regex match object
            jobsite_name_res = reg_job.search(line)
            building_level_network_name_res = reg_bln.search(line)
            fieldpanel_name_res = reg_field.search(line)
            instance_number_res = reg_instance.search(line)
            field_level_network_name_res = reg_fln.search(line)
            device_name_res = reg_device.search(line)
            application_number_res = reg_app.search(line)
            drop_number_res = reg_drop.search(line)

            # Each regex match object has useful attributes and methods
            # re.match.end() : (int) position of end of string matched by match object
            if jobsite_name_res:
                jobsite_pos = jobsite_name_res.end()
                jobsite_name = line[jobsite_pos:-1]  # Return string
                jobsite_name = jobsite_name.strip()  # Clean string
                # Add to dictionary struct
                bln_dict[jobsite_name] = {}

            if building_level_network_name_res:
                bln_name_position = building_level_network_name_res.end()
                building_level_network_name = line[bln_name_position:-1]  # Return string
                building_level_network_name = building_level_network_name.strip()  # Clean string
                # Add to dictionary struct
                bln_dict[jobsite_name][building_level_network_name] = {}
            
            if fieldpanel_name_res:
                fieldpanel_name_pos = fieldpanel_name_res.end()
                fieldpanel_name = line[fieldpanel_name_pos:-1]  # Return string
                fieldpanel_name = fieldpanel_name.strip()  # Clean string
                # Add to dictionary struct
                bln_dict[jobsite_name][building_level_network_name][fieldpanel_name] = {}

            # This script is not sufficient to differentiate when there are multiple 
            # 'Device Instance' strings in the report
            if instance_number_res:
                instance_pos = instance_number_res.end()
                instance_name = line[instance_pos:-1]
                instance_name = instance_name.strip()
                # TODO - what if there are instance under FLN devices and BLN devices?
                bln_dict[jobsite_name][building_level_network_name][fieldpanel_name]['instance'] = instance_name

            if field_level_network_name_res:
                fln_pos = field_level_network_name_res.end()
                field_level_network_name = line[fln_pos:-1]
                field_level_network_name = 'FLN' + field_level_network_name.strip()
                bln_dict[jobsite_name][building_level_network_name][fieldpanel_name][field_level_network_name] = {}

            if device_name_res:
                device_name_res_pos = device_name_res.end()
                device_name = line[device_name_res_pos:-1]
                device_name = device_name.strip()
                bln_dict[jobsite_name][building_level_network_name][fieldpanel_name][field_level_network_name][device_name] = {}

            if application_number_res:
                application_number_res_pos = application_number_res.end()
                application_name = line[application_number_res_pos:-1]
                application_name = application_name.strip()
                bln_dict[jobsite_name][building_level_network_name][fieldpanel_name][field_level_network_name][device_name]['application'] = application_name

            if drop_number_res:
                drop_pos = drop_number_res.end()
                drop_name = line[drop_pos:-1]
                drop_name = drop_name.strip()
                bln_dict[jobsite_name][building_level_network_name][fieldpanel_name][field_level_network_name][device_name]['drop'] = drop_name

    return bln_dict

def write_bln_dictionary_to_file(bln_dictionary:BLN_DICT, filepath:str):
    """Write a nested dictionary to csv file"""
    header:List[str] = ['Jobsite name','Building level network name','Field panel name','Field level network name','Device name','Application number','Drop']
    with open(filepath, 'wt', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        # BLN stands for 'building level network'
        for jobsite_name, BLN_dict_level1 in bln_dictionary.items():
            for bln_name, field_panel_dict_level2 in BLN_dict_level1.items():
                for field_panel_name, fln_dict_level3 in field_panel_dict_level2.items():
                    for field_level_network_name, field_level_network_dict_level4 in fln_dict_level3.items():
                        for device_name, device_dict_level5 in field_level_network_dict_level4.items():
                            try:
                                application_number = device_dict_level5['application']
                            except KeyError:
                                application_number = 'NA'
                            try:
                                drop_number = device_dict_level5['drop']
                            except KeyError:
                                drop_number = 'NA'
                            row:List[str] = [jobsite_name,bln_name,field_panel_name,field_level_network_name,device_name,application_number,drop_number]
                            writer.writerow(row)
    return None

