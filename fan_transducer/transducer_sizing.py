# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:14:47 2019

@author: john vorsten
"""
# Python imports
import operator
import math

# Third party imports
import numpy as np

# local imports

# Declarations
POUND_MASS_GRAVITATIONAL_CONSTANT = 32.174  # [lbm*ft/s^2]
WATER_FORCE = 5.1972 # [lbf / (ft^2 * inch water column)]


# %%


def calc_flow(orifice_constant,
              differential_pressure,
              area,
              method='standard_density',
              density=0.075):
    """inputs
    -------
    C1: (float) Orifice inlet constant
    dp: (float) measured differential pressure [inches water column]
    area: Inlet throat area (for fan) @ pressure tap. To use standard density
    method set area = None [ft^2]
    method: (str) 'standard_density' or 'non_standard_density'. standard
    density method calculates flow rate given an orifice constant and measured
    differential pressure. Non-standard method is the non-standard air density
    method. It calculates flow rate and corrects differential pressure with
    a measured density.
    density: air density (default 0.075 lb/ft^3). To use Standard Density Method
    set density = None
    output
    -------
    ACMF: Calculated fan flow [ft^3/min]"""

    if operator.xor(area, density):
        raise ValueError('Incorrect invocation of airlfow calculation function\
                         set both area and density = None or define')

    # Non-standard density method
    if all((bool(area), bool(density), method == 'non_standard_density')):
        flow_rate = orifice_constant * area * \
            np.sqrt(differential_pressure/density)

    # Standard density method
    elif all((area is None, density is None, method == 'standard_density')):
        flow_rate = orifice_constant * np.sqrt(differential_pressure)

    else:
        raise ValueError("Incorrect function parameters passed. Check method\
                         argument")

    return flow_rate


def calc_dp(flow_rate: float, C1: float, area: float, density: float = 0.075) -> float:
    """Calculate velocity pressure of an air stream using the non-standard
    density method, or standard density method
    inputs
    -------
    flow_rate: (float) [ft^3/min] expected flow rate 
    C1: (float) [unitless] Orifice inlet constant
    area: (float) [ft^2] Inlet throat area (for fan) @ pressure tap. To use standard density method
    set area = None
    density: (float) [lb/ft^3] air density (default 0.075 lb/ft^3). To use Standard Density Method
    set density = None
    output
    -------
    vp: (float) [inches water column] velocity pressure of an air stream"""

    if operator.xor(bool(area), bool(density)):
        raise ValueError('Incorrect invocation of airflow calculation function\
                         set both area and density = None or define')

    # Non-standard density method
    if all((bool(area), bool(density))):
        vp = ((flow_rate / C1 / area) ** 2) / density

    # Standard density method
    vp = calc_dp_standard_density(flow_rate, C1)

    return vp


def calc_dp_standard_density(flow_rate: float, C1: float):
    """Calculate velocity pressure of an airstream using standard
    density method where 
    (velocity pressure) = (flow rate / orifice constant) ** 2
    inputs
    -------
    flow_rate: (float) [ft^3/min] expected flow rate 
    C1: (float) Orifice inlet constant
    outputs
    -------
    vp: (float) [inches water column] velocity pressure"""

    # Standard density method
    vp = (flow_rate / C1) ** 2

    return vp


def clac_dp_non_standard_density(flow_rate: float, C1: float, area: float, density: float = 0.075) -> float:
    """Calculate velocity pressure of an airstream using non-standard
    density method where
    velocity pressure = ((flow rate / (orifice constant * area) ** 2)) / density
    inputs
    -------
    flow_rate: (float) [ft^3/min] expected flow rate 
    C1: (float) Orifice inlet constant
    area: (float) [ft^2] Inlet throat area (for fan) @ pressure tap
    density: (float) [lb/ft^3] air density (default 0.075 lb/ft^3)
    outputs
    -------
    vp: (float) velocity pressure"""

    # Non-standard density method
    if all((bool(area), bool(density))):
        vp = ((flow_rate / C1 / area) ** 2) / density
    return None


def calc_velocity_pressure(diameter: float, airflow: float, density=0.0763) -> float:
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
    diameter: (float) duct diameter in [inch]
    airflow: (float) airflow in [ft^3/min]
    density: (float) density of air in [lbm / ft^3]"""

    area = math.pi * (diameter / 2 / 12) ** 2  # [ft^2]
    velocity = (airflow / 60) / area  # [ft^sec]
    pressure = (0.5 * density * (velocity) ** 2) / (POUND_MASS_GRAVITATIONAL_CONSTANT * WATER_FORCE)  # [lbf/ft^2]

    return pressure


def calc_velocity_pressure_conversion_constant(diameter: float, airflow: float, conversion_constant=3970) -> float:
    """
    Calculate the velocity pressure of an air stream using a conversion
    constant. Default conversion constant is 3970 at 60 DEG F airflow. This
    constant varies up to 4005 at 77 DEG F air. The conversion constant acts
    as a an assumption on the air density

    inputs
    -------
    diameter: (float) duct diameter in [inch]
    airflow: (float) airflow in [ft^3/min]
    conversion_constant: (float) conversion constant, 3970 @ 60 DEG F, 4005@77 DEG F
    For standard air (standard temperature and pressure), air density is assumed
    to be 0.074 [lbm / ft^3].

    Air velocity = (2 * velocity pressure * inch water column conversion * pound mass to pound force conversion * seconds to minute) / (density)) ** (1/2)
    Air velocity = 4005 * (velocity pressure) ** (1/2)
    IP units: velocity pressure [inches water column]
    air velocity = (2 * (velocity pressure) / (density)) ** (1/2)
    velocity pressure [in H2O] = (velocity / conversion_constant) ** 2"""

    area = math.pi * (diameter / 2 / 12) ** 2  # [ft^2]
    velocity = (airflow) / area  # [ft^3/minute] / [ft^2] = [ft/min]
    pressure = (velocity / conversion_constant) ** 2 # ([ft/min] / [unitless]) ** 2 = [ft^2 / min^2]

    return pressure
