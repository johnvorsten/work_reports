"""
Test for module transducer_sizing
author: john vorsten
date: 2022-5-20
"""
# %%

# Python imports
import unittest
import math

# Third party imports

# Local imports
from calculators.bernoulli_liquid_flow import (
    calc_velocity_pressure,
    calc_velocity_pressure_standard_density,
    calc_velocity_pressure_conversion_constant,
    calc_volumetric_airflow,
    calc_volumetric_airflow_standard_density,
    orifice_mass_flow,
)

# Declarations


# %%


class TestTransducerSizing(unittest.TestCase):
    """Test methods defined in transducer_sizing.py"""

    def test_calc_dp_standard_density(self):
        """Calculate the expected differential pressure reading with an orifice constant
        of C1"""
        # Fan Area
        DIAMETER = 8  # [in]
        AREA = math.pi*(DIAMETER / 2) ** 2  # [in^2]

        # Orifice constant
        # From fan manufacturer
        # 5.5 HP
        # 4 pole 1750 rpm
        # 460/3/60
        # diameter 20
        # width 65
        # HPF-A100 wheel
        # 88% efficiency motor
        # cone constant 2524
        # cone dp = 6.75 in h20 @ 6632 CFM
        C1 = 2524  # Example

        # Minimum expected CFM
        MIN_CFM = 4200  # [ft^3/min]

        # Expected maximum CFM
        MAX_CFM = 6632  # [ft^3/min]

        # Expected transducer pressure at minimum expected cfm
        minimum_dp = calc_velocity_pressure_standard_density(MIN_CFM, C1)
        print('calculated dp : ', minimum_dp)

        # Expected transducer pressure at maximum expected cfm
        maximum_dp = calc_velocity_pressure_standard_density(MAX_CFM, C1)
        print('calculated dp : ', maximum_dp)

        # inches of water column
        self.assertAlmostEqual(minimum_dp, 2.7689, places=3)
        # inches of water column
        self.assertAlmostEqual(maximum_dp, 6.9041, places=3)

        return None

    def test_calc_velocity_pressure(self):
        """Typical velocity pressure for a terminal unit"""

        diameter = 4  # inches
        max_cfm = 50  # ft^3/min
        min_cfm = 17  # ft^3/min
        area = math.pi * (diameter / 2 / 12) ** 2  # [ft^2]
        max_p = calc_velocity_pressure(area, max_cfm)
        min_p = calc_velocity_pressure(area, min_cfm)
        print("Velocity pressure [lbf/ft^2] at diameter={} [in], flow={} [ft^3/min] | {}".format(
            diameter, max_cfm, max_p))
        print("Velocity pressure [lbf/ft^2] at diameter={} [in], flow={} [ft^3/min] | {}".format(
            diameter, min_cfm, min_p))

        # inches water column
        self.assertAlmostEqual(max_p, 0.020177, places=3)
        # inches water column
        self.assertAlmostEqual(min_p, 0.002405, places=3)

        return None

    def test_calc_velocity_pressure_conversion_constant(self):
        """Velocity pressure of an airstream using a conversion constant"""

        diameter = 4  # inches
        max_cfm = 50  # ft^3/min
        min_cfm = 17  # ft^3/min
        area = math.pi * (diameter / 2 / 12) ** 2  # [ft^2]
        max_p = calc_velocity_pressure_conversion_constant(
            area, max_cfm, conversion_constant=4005)
        min_p = calc_velocity_pressure_conversion_constant(
            area, min_cfm, conversion_constant=4005)
        print("Velocity pressure [lbf/ft^2] at diameter={} [in], flow={} [ft^3/min] | {}".format(
            diameter, max_cfm, max_p))
        print("Velocity pressure [lbf/ft^2] at diameter={} [in], flow={} [ft^3/min] | {}".format(
            diameter, min_cfm, min_p))

        # inches water column
        self.assertAlmostEqual(max_p, 0.020466, places=3)
        # inches water column
        self.assertAlmostEqual(min_p, 0.002365, places=3)

        return None

    def test_calc_volumetric_airflow(self):
        """Volumetric airflow with specified density"""

        diameter = 4  # inches
        velocity_pressure = 0.020804  # Approximately 50 CFM
        density = 0.074
        area = math.pi * (diameter / 2 / 12) ** 2  # [ft^2]

        volumetric_ariflow = calc_volumetric_airflow(
            area, velocity_pressure, density)

        self.assertAlmostEqual(volumetric_ariflow, 50.77,
                               places=1)  # inches water column

        return None

    def test_calc_volumetric_airflow_standard_density(self):
        """Volumetric airflow with standard density"""

        diameter = 4  # inches
        velocity_pressure = 0.020804  # Approximately 50 CFM
        orifice_constant = 4005
        area = math.pi * (diameter / 2 / 12) ** 2  # [ft^2]

        volumetric_ariflow = calc_volumetric_airflow_standard_density(
            area, velocity_pressure, orifice_constant)

        self.assertAlmostEqual(volumetric_ariflow, 50.41,
                               places=1)  # inches water column
        return None

    def test_orifice_mass_flow(self):
        """Calculate mass flow rate through an orifice given an orifice constant,
        differential pressure across the orifice, and liquid density"""

        flow_coeff = 0.6  # [units]
        inlet_pipe_diameter = 0.1  # [meters]
        orifice_pipe_diameter = 0.05  # [meters]
        inlet_pressure = 100000  # pa
        orifice_pressure = 80000  # pa
        density = 1000  # [kg/m^3]
        mass_flow = orifice_mass_flow(
            flow_coeff,
            inlet_pipe_diameter,
            orifice_pipe_diameter,
            inlet_pressure,
            orifice_pressure,
            density)

        self.assertAlmostEqual(mass_flow, 7.21434, places=3)
        return None


if __name__ == '__main__':
    unittest.main()
# %%
