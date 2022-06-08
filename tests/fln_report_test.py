# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:15:43 2020

@author: z003vrzk
"""
# Python Imports
import unittest

# Local imports
from text_parsing.fln_report_parser import create_bln_dict, bln_dict_to_df

# Declarations
FLN_REPORT_FILEPATH = './tests/fln_report_test.txt'

# %%

class FLNReportTest(unittest.TestCase):

    def test_create_bln_dict(self):
        """"""
        # Create dictionary of BLN profile
        bln_dict = create_bln_dict(FLN_REPORT_FILEPATH)

        return None

    def test_bln_dict_to_df(self):
        """"""
        # Create dictionary of BLN profile
        bln_dict = create_bln_dict(FLN_REPORT_FILEPATH)

        # Convert dictionary of BLN profile to dataframe for report generation
        fln_dataframe = bln_dict_to_df(bln_dict)
        return None

if __name__ == '__main__':
    unittest.main()