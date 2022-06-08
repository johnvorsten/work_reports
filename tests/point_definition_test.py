"""Test module point_definition_parser.py"""
# Python Imports
from ctypes.wintypes import POINT
from re import match
import unittest
import re
from typing import List
import os

# Local imports
from text_parsing.point_definition_parser import (
    _trim_and_strip_text,
    _find_file_primary_key_start_lines,
    _parse_text_from_offset_to_offset,
    parse_text_to_list,
    write_dataclass_to_csv,
    regex_searches,
    PointDefinition)

# Declarations
POINT_DEFINITION_FILEPATH = './tests/point_definition_test.txt'
SAVE_FILEPATH = './tests/point_definition_test.csv'
TEST_TEXT = """
4/27/2022
                  Point Definition Report ( Temporary Report )

Selection:  B01.4307.FR7.STAEFA.COMFAIL, B01.4307.RF5.STAEFA.COMFAIL, ...
(863 Points)
________________________________________________________________________________

Point System Name:       B01.4307.FR7.STAEFA.COMFAIL
Point Name:              B01.4307.FR7.STAEFA.COMFAIL
Point Type:              LDO
Supervised:              No

                                     - 1 -

Point System Name:       B01.4307.RF5.STAEFA.COMFAIL

********************************************************************************

4/27/2022                   Powers of johnathan vorsten                   04:14 PM
                  Point Definition Report ( Temporary Report )

Selection:  f iu3qotoh 4q3876t gb3 bnkj
(863 Points)
________________________________________________________________________________

Point System Name:       B01.4325.RF6.STAEFA.COMFAIL
"""
DUMMY_POINT = PointDefinition(
    point_system_name='B01.4307.FR7.STAEFA.COMFAIL',
    point_name='B01.4307.FR7.STAEFA.COMFAIL',
    point_type='LDO',
    supervised='No',
    revision_number='12', classification='Building Automation', 
    descriptor='CRITALM COMFAIL', 
    panel_name='B03.4331a.MBC01 (BASB04PR-25)', 
    point_address='-Virtual-', 
    slope='', 
    cov_limit='', 
    engineering_units='', 
    analog_representation='', 
    text_table='NORMAL_ALARM', 
    initial_value='NORMAL', 
    totalization='None           Initial Priority:   NONE', 
    enabled_for_reno='Yes', 
    alarm_issue_management='No', 
    graphic_name='<Undefined>', 
    informational_text='<< No Text Defined >>', 
    alarm_type='Enhanced Alarms', 
    alarm_count_2='No', 
    normal_ack_enabled='Yes', 
    print_info_with_alarm='Yes            Print Alarms on BLN:Yes', 
    mode_point='B03.4331a.MBC01.MODE', 
    mode_delay_min='0', 
    default_destination_1='1 (SUPERVISOR)', 
    default_destination_2='2 (PATIENT CARE MAIN)', 
    default_destination_3='<Undefined>', 
    default_destination_4='<Undefined>',
    alarm_mode='Night Mode (0)')

# %%


class TestPointDefinitionParser(unittest.TestCase):

    def setUp(self):
        return None

    def test__trim_and_strip_text(self):
        """"""
        # Dummy line for regex matching
        line: str = 'Point System Name:       B01.4307.FR7.STAEFA.COMFAIL'
        regex: re.Pattern = regex_searches[0]
        match: re.match = regex.search(line)
        result = _trim_and_strip_text(match, line)
        self.assertEqual(result, 'B01.4307.FR7.STAEFA.COMFAIL')

        return None

    def test__find_file_primary_key_start_lines(self):
        """"""
        byte_offsets: List[int] = _find_file_primary_key_start_lines(
            POINT_DEFINITION_FILEPATH)
        self.assertEqual(byte_offsets[0], 330)
        self.assertEqual(byte_offsets[1], 2330)
        self.assertListEqual(
            byte_offsets, [330, 2330, 4330, 6329, 7299, 8650, 9524, 10775])

        return None

    def test__parse_text_from_offset_to_offset(self):
        """"""
        byte_offsets: List[int] = _find_file_primary_key_start_lines(
            POINT_DEFINITION_FILEPATH)

        with open(POINT_DEFINITION_FILEPATH, 'rt', encoding='UTF-8') as file:
            point: PointDefinition = _parse_text_from_offset_to_offset(
                file, byte_offsets[0], byte_offsets[1])

        self.assertEqual(point, DUMMY_POINT)

        return None

    def test_parse_text_to_list(self):
        """"""
        points: List[PointDefinition] = parse_text_to_list(
            POINT_DEFINITION_FILEPATH)

        return None

    def test_write_dataclass_to_csv(self):
        """"""
        points: List[PointDefinition] = parse_text_to_list(
            POINT_DEFINITION_FILEPATH)
        write_dataclass_to_csv(SAVE_FILEPATH, points)

        os.remove(SAVE_FILEPATH)

        return None


if __name__ == '__main__':
    unittest.main()
