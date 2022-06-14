# Description
Collection of automation scripts and tools

# Modules and tools logical groupings

## text_parsing directory
* fln_report_main.py
* point_definition_main.py

### Usage instructions
Please note that installation packages are not defined within this project. There is no `__main__.py` entrypoint or pip install file which allows this package to be installed and then called by looking at sys.path. This means you must manually clone the repository, navigate to repository root, then execute scripts as modules.

To parse a point definition report (see sample point_definition_test.txt under tests/):
1. Navigate to project root (work_reports/)
2. Execute `python -m text_parsing.point_definition_main`

To parse a FLN report (see sample fln_report_test.txt under tests/):
1. Navigate to project root (work_reports/)
2. Execute `python -m text_parsing.fln_report_main`

## other-scripts
* batch_change_file_attributes.py - set file attributes under a directory recursively
* batch_change_file_name.py - Change file names that match a pattern under a directory recursively
* change_point_address.py - Interface to Microsoft SQL server that changes certain data
* empty_directory.py - Empty files under a directory that matches a certain pattern

## calculators
* bernoulli_liquid_flow.py - Calculations related to volumetric liquid flow (bernoulli stream flow)
* coil_power_calculator.py - Calculations related to heat rate from air to water heat exchanger coils 
* coil_sizing.py - Calculations related to heat rate from air to water heat exchanger coils 
* room_airflow_calculator.py - Minimization of a variable given constraints

## ABT
Scripts to parse unknown structured data (non-functional)

## acad printer
Printing using autocad software (non-functional)

## Testing
python -m unittest tests