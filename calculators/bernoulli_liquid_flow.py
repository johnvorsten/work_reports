# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:14:47 2019

@author: john vorsten
"""
# Python imports
import operator
import math

# Third party imports

# local imports

# Declarations
POUND_MASS_GRAVITATIONAL_CONSTANT = 32.174  # [lbm * ft / s^2]
WATER_FORCE = 5.1972  # [lbf / (ft^2 * inch water column)]
STANDARD_AIR_DENSITY = 0.074  # [lbm / ft^3]
# 3970 @ 60 DEG F, 4005@77 DEG F
# [ft / (minute * inches water column)]
STANDARD_AIR_CONVERSION_CONSTANT = 4005


# %%

def calc_volumetric_airflow(
        area: float,
        velocity_pressure: float,
        density: float = STANDARD_AIR_DENSITY) -> float:
    """Calculate volumetric airflow rate of an airstream using standard
    density method where
    volumetric airflow = orifice constant * area * (velocity pressure ** (1/2))

    inputs
    -------
    area: (float) [ft^3/min] expected flow rate 
    velocity_pressure: (float) [inches of water column] velocity pressure of air stream
    density: (float) [lbm / ft^3] density of airflow

    outputs
    -------
    volumetric_airflow: (float) [ft^3/min] volumetric airflow rate"""

    # Standard density method
    volumetric_airflow = area * \
        math.sqrt((2 * velocity_pressure * WATER_FORCE *
                  POUND_MASS_GRAVITATIONAL_CONSTANT * (60 ** 2)) / density)

    return volumetric_airflow


def calc_volumetric_airflow_standard_density(
        area: float,
        velocity_pressure: float,
        orifice_constant: float) -> float:
    """Calculate volumetric airflow rate of an airstream using standard
    density method where
    volumetric airflow = orifice constant * area * (velocity pressure ** (1/2))

    inputs
    -------
    area: (float) [ft^3/min] expected flow rate 
    velocity_pressure: (float) [inches of water column] velocity pressure of air stream
    orifice_constant: (float) [ft / (minute * inches water column)] Orifice inlet constant

    outputs
    -------
    volumetric_airflow: (float) [ft^3/min] volumetric airflow rate"""

    # Standard density method
    volumetric_airflow = area * orifice_constant * math.sqrt(velocity_pressure)

    return volumetric_airflow


def calc_velocity_pressure_standard_density(
        volumetric_ariflow_rate: float,
        orifice_constant: float):
    """Calculate velocity pressure of an airstream using standard
    density method where 
    (velocity pressure) = (flow rate / orifice constant) ** 2
    In this example, the orifice constant is a combined constant which includes
    the area of the orifice
    inputs
    -------
    volumetric_ariflow_rate: (float) [ft^3/min] expected flow rate 
    orifice_constant: (float) Orifice inlet constant
    outputs
    -------
    vp: (float) [inches water column] velocity pressure"""

    # Standard density method
    velocity_pressure = (volumetric_ariflow_rate / orifice_constant) ** 2

    return velocity_pressure


def calc_velocity_pressure(
        area: float,
        volumetric_ariflow_rate: float,
        density=STANDARD_AIR_DENSITY) -> float:
    """Calculate velocity pressure given duct diameter and ariflow
    air density is the density of air with units [lbm/ft^3]. Air density varies with
    temperature
    velocity pressure = (1/2 * density * velocity ** 2) / (air mass conversion)

    Velocity = ( 2 * velocity pressure * pounds force per area inch of water column * pound mass gravitational constant * seconds per minute) / (air density) ) ** (1/2)
    Velocity = ( 2 * pv * 5.1972 * 32.174 * 3600) / (0.763) ) ** (1/2)
    Velocity= 4005 * (velocity pressure) ** (1/2)

    velocity pressure = (1/2) * (air density) * (velocity ** 2) / (pounds force per area inch of water column * pound mass gravitational constant * seconds per minute)

    inputs
    -------
    area: (float) duct inlet area in [ft^2]
    volumetric_ariflow_rate: (float) airflow in [ft^3/min]
    density: (float) density of air in [lbm / ft^3]"""

    velocity = (volumetric_ariflow_rate / 60) / area  # [ft^sec]
    pressure = (0.5 * density * (velocity) ** 2) / \
        (POUND_MASS_GRAVITATIONAL_CONSTANT * WATER_FORCE)  # [lbf/ft^2]

    return pressure


def calc_velocity_pressure_conversion_constant(
        area: float,
        volumetric_ariflow_rate: float,
        conversion_constant=STANDARD_AIR_CONVERSION_CONSTANT) -> float:
    """
    Calculate the velocity pressure of an air stream using a conversion
    constant. Default conversion constant is 3970 at 60 DEG F airflow. This
    constant varies up to 4005 at 77 DEG F air. The conversion constant acts
    as a an assumption on the air density

    inputs
    -------
    area: (float) duct inlet area in [ft^2]
    volumetric_ariflow_rate: (float) airflow in [ft^3/min]
    conversion_constant: (float) [ft / (minute * inches water column)] conversion constant, 3970 @ 60 DEG F, 4005@77 DEG F
    For standard air (standard temperature and pressure), air density is assumed
    to be 0.074 [lbm / ft^3].

    Air velocity = (2 * velocity pressure * inch water column conversion * pound mass to pound force conversion * seconds to minute) / (density)) ** (1/2)
    Air velocity = 4005 * (velocity pressure) ** (1/2)
    IP units: velocity pressure [inches water column]
    air velocity = (2 * (velocity pressure) / (density)) ** (1/2)
    velocity pressure [in H2O] = (velocity / conversion_constant) ** 2"""

    # [ft^3/minute] / [ft^2] = [ft/min]
    velocity = (volumetric_ariflow_rate) / area
    # ([ft/min] / [unitless]) ** 2 = [ft^2 / min^2]
    pressure = (velocity / conversion_constant) ** 2

    return pressure


def orifice_mass_flow(
        orifice_constant: float,
        diameter_inlet: float,
        diameter_orifice: float,
        free_flow_pressure: float,
        orifice_pressure: float,
        liquid_density: float) -> float:
    """Calculate mass flow rate through an orifice given an orifice constant,
    differential pressure across the orifice, and liquid density

    inputs
    -------
    orifice_constant: (float) orifice constant
    diameter_inlet, diameter_orifice: (float) diameter of inlet pipe (d1), and diameter of orifice 
    reduced area (d2)
    free_flow_pressure, orifice_pressure: (float) pressure measured in free flow (p1), and pressure measured
    after orifice (p2)
    liquid_density: (float) liquid density"""

    assert free_flow_pressure > orifice_pressure, 'Inlet pressure must be greater than low side pressure'

    mass_flow = (
        orifice_constant * (math.pi/4) * (diameter_orifice**2) * liquid_density *
        (2 * (free_flow_pressure-orifice_pressure) / liquid_density *
         (1 - (diameter_orifice/diameter_inlet)**4)) ** (1/2)
    )

    return mass_flow
