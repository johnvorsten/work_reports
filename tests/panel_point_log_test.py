"""Test module point_definition_parser.py"""
# Python Imports
from re import match
import unittest
import re
from typing import List, Dict
import os

# Local imports
from text_parsing.panel_point_log_parser import (
    _trim_and_strip_text,
    write_dataclass_to_csv,
    parse_text_to_pointdefinition_list,
    _parse_object_line,
    _determine_header_start_positions,
    _line_is_asterisk,
    _line_is_header,
    _line_is_list_end,
    HEADERS_START as parsers_HEADERS_START,
    PointDefinition)

# Declarations
POINT_DEFINITION_FILEPATH = './tests/point_log_report_test.txt'
SAVE_FILEPATH = './tests/point_log_report_test.csv'

DUMMY_POINT = PointDefinition(
    name='POINT.NAME.SYSTEM',
    address='1 01 01',
    description='POINT BELONGING TO SYSTEM',
    value='0.00',
    status='-N-',
    priority='NONE',
)
HEADERS_START: Dict[str, int] = {
    'Name:Suffix':0,
    'Address':30,
    'Description':46,
    'Value/State':65,
    'Status':83,
    'Priority':91}

# %%


class TestPointDefinitionParser(unittest.TestCase):

    def setUp(self):
        """"""
        return None

    def test__determine_header_start_positions(self):
        """"""
        line = 'Name:Suffix                   Address         Description        Value/State       Status  Priority'
        _determine_header_start_positions(line)
        self.assertEqual(parsers_HEADERS_START['Name:Suffix'], 0)
        self.assertEqual(parsers_HEADERS_START['Address'], 30)
        self.assertEqual(parsers_HEADERS_START['Description'], 46)
        self.assertEqual(parsers_HEADERS_START['Value/State'], 65)
        self.assertEqual(parsers_HEADERS_START['Status'], 83)
        self.assertEqual(parsers_HEADERS_START['Priority'], 91)

        return None

    def test__line_is_header(self):
        """"""
        line = 'Name:Suffix                   Address         Description        Value/State       Status  Priority'
        self.assertTrue(_line_is_header(line))
        return None

    def test__line_is_list_end(self):
        previous_line = '****************************************************************************************************'
        line = ''
        self.assertTrue(_line_is_list_end(line, previous_line))
        self.assertTrue(_line_is_list_end('\n', previous_line))

        return None

    def test__line_is_asterisk(self):
        line = '****************************************************************************************************'
        self.assertTrue(_line_is_asterisk(line))
        return None

    def test__parse_object_line(self):
        line = 'B01.4392a.FR2.STAEFA.COMFAIL  -Virtual-       (CRITALM COMFAIL ) NORMAL             -N-       NONE '
        point = _parse_object_line(line, HEADERS_START)
        self.assertEqual(point.name, 'B01.4392a.FR2.STAEFA.COMFAIL')
        self.assertEqual(point.address, '-Virtual-')
        self.assertEqual(point.description, '(CRITALM COMFAIL )')
        self.assertEqual(point.value, 'NORMAL')
        self.assertEqual(point.status, '-N-')
        self.assertEqual(point.priority, 'NONE')

        return None

    def test__trim_and_strip_text(self):
        """"""
        # Dummy line for regex matching
        line: str = 'B01.4307.RF5.STAEFA.COMFAIL   -Virtual-       (CRITALM COMFAIL ) NORMAL             -N-       NONE'
        start: int = 30
        end: int = 39
        result = _trim_and_strip_text(line, start, end)
        self.assertEqual(result, '-Virtual-')

        return None

    def test_write_dataclass_to_csv(self):
        """"""
        points: List[PointDefinition] = parse_text_to_pointdefinition_list(
            POINT_DEFINITION_FILEPATH)
        write_dataclass_to_csv(SAVE_FILEPATH, points)

        os.remove(SAVE_FILEPATH)

        return None


if __name__ == '__main__':
    unittest.main()
