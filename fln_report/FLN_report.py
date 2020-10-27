# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:34:54 2019

@author: z003vrzk
"""


"""
The text file report from commissioning tool has the following nested format :
The report name is "system profile report" and export the report as a text file

<Job Site:>
<BLN:>
    <Field Panel : (name, descriptor, node ID, etc)>
        <FLN : (number, descriptor)>
            <FLN Device : >
                <Application : >
                <Drop : >
                    
fln_dict = {'Job Site:':
    {'BLN':
        {'Field Panel:':
            {'FLN:':
                {'FLN Device:':
                    {'Application':0, 'Drop':1}}}}}}
    
dev_dict = {'Application':0, 'Drop':0}
fln_dict = {<fln_device_name>:dev_dict}
field_dict = {<fln_number>:fln_dict, <instance>:instance}
"""
                    
import re
import pandas as pd


#%% Main function


def create_bln_dict(file_path):
    """Outputs a dictionary structure after iterating through all lines in an
    input text file. The output dict represents the network FLN structure
    of the text file. The text file is the "system profile" report
    in commissioning tool
    inptus
    -------
    file_path : (str) .txt file of 'system profile' report from commissiong tool
    outputs
    -------
    bln_dict : (dict) representing structured network heirarchy
    bln_dict = {'Job Site:':
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
    reg_fln = re.compile('FLN:')
    reg_device = re.compile('FLN Device:')
    reg_app = re.compile('Application:')
    reg_drop = re.compile('Drop:')
    reg_space = re.compile(': ')
    
    
    # result = regex.match(string)
    bln_dict = {}
    
    with open(file_path, 'r') as f:
        for line in f:
            
            # Each regex pattern search result returns a regex match object
            field_res = reg_field.search(line)
            instance_res = reg_instance.search(line)
            fln_res = reg_fln.search(line)
            dev_res = reg_device.search(line)
            app_res = reg_app.search(line)
            drop_res = reg_drop.search(line)
            
            # Each regex match object has useful attributes and methods
            # re.match.end() : (int) position of end of string matched by match object
            if field_res:
                field_pos = field_res.end()
                field_name = line[field_pos:-1] # Return string
                field_name = field_name.strip() # Clean string
                bln_dict[field_name] = {'instance':0} # Add to dictionary struct
            
            if instance_res:
                instance_pos = instance_res.end()
                instance_name = line[instance_pos:-1]
                instance_name = instance_name.strip()
                bln_dict[field_name]['instance'] = instance_name
                
            if fln_res:
                fln_pos = fln_res.end()
                fln_name =  line[fln_pos:-1]
                fln_name = 'FLN' + fln_name.strip()
                bln_dict[field_name][fln_name] = {}
    
            if dev_res:
                dev_pos = dev_res.end()
                dev_name = line[dev_pos:-1]
                dev_name = dev_name.strip()
                bln_dict[field_name][fln_name][dev_name] = {}
    
            if app_res:
                app_pos = app_res.end()
                app_name = line[app_pos:-1]
                app_name = app_name.strip()
                bln_dict[field_name][fln_name][dev_name]['application'] = app_name
    
            if drop_res:
                drop_pos = drop_res.end()
                drop_name = line[drop_pos:-1]
                drop_name = drop_name.strip()
                bln_dict[field_name][fln_name][dev_name]['drop'] = drop_name
                
    return bln_dict


def bln_dict_to_df(bln_dictionary):
    """ Outputs a pandas dataframe from a structured, nested hash table
    Inputs
    -------
    bln_dictionary : (dict) dictionary output from create_bln_dict
    outputs
    -------
    master_df : (pd.DataFrame) dataframe with rows and columns as would be
    expected in a typical fln report"""
    
    master_df = pd.DataFrame()
    
    # Convert dictioanry to dataframe
    for field_panel, fln_dict in bln_dictionary.items():
        
        for fln, device_dict in fln_dict.items():
            
            if isinstance(device_dict, dict):
                # Each save_dict is a row in the .csv file
                save_dict = bln_dictionary[field_panel][fln]
                
                # Convert dictionary to row of dataframe
                save_df = pd.DataFrame.from_dict(save_dict, orient='index')
                save_df.insert(value=[fln]*len(save_dict.keys()), 
                               loc=len(save_df.columns), 
                               column='FLN')
                save_df.insert(value=[field_panel]*len(save_dict.keys()), 
                               loc=len(save_df.columns), 
                               column='Field Panel')
                save_df.reset_index(inplace=True)
                save_df = save_df.rename(columns={'index':'System Name'})
                master_df = master_df.append(save_df)
            else:
                continue
            
    return master_df

        





