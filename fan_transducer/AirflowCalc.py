# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 10:04:31 2019

This script is used to calculate airflow using pressure.

There are (3) methods provided in this file.
(1) velocity_air_flow
Given differential pressure and an inlet diameter calculate the flow rate of
a liquid
This function assumes differential presssure is input in inches of water column
and channel diameter is in inches

pressure_airflow
Given a flow rate [ft^3/min], calculate the velocity pressure at the sensor 
[inches water column]

orifice_mass_flow



@author: z003vrzk
"""


def calculate_volumetric_flow(channel_diameter, 
                      differential_pressure, 
                      k=4005, 
                      flow_coefficient=1):
    """Calculates volumetric flow arte from differential pressure
    and duct inlet size 
    parameters
    -------
    d1 : inlet diameter [inches]
    diff_p : measured pressure [inches WC]
    box_coef : linear scale between ideal and real conditions
    k : conversion between pressure and velocity, f(density,temp)"""
    pi = 3.141592653589793
    Area = pi*(channel_diameter / 2  /12)**(2)
    velocity = k * (differential_pressure ** (1/2))
    flow_rate = velocity * Area * flow_coefficient
    return flow_rate



def calculate_velocity_pressure(channel_diameter, 
                     flow, 
                     k=4005, 
                     box_coef=1):
    """Calculates differential pressure from volumetric flow rate
    and duct inlet size 
    parameters
    -------
    d1 : inlet diameter [inches]
    flow : measured flow [ft^3/minute]
    box_coef : linear scale between ideal and real conditions
    k : conversion between pressure and velocity, f(density,temp)"""
    
    pi = 3.141592653589793
    Area = pi*(channel_diameter / 2 / 12)**(2)
    
    velocity = flow / box_coef / Area
    
    differential_pressure = (velocity / k)**2
    
    return differential_pressure



"""Orifice flow"""
def orifice_mass_flow(k, d1, d2, p1, p2, rho):
    """Calculate mass flow rate through an orifice given an orifice constant,
    differential presssure across the orifice, and liquid denisty
    
    inputs
    -------
    k : (float) orifice constant
    d1, d2 : (float) diameter of inlet pipe (d1), and diameter of orifice 
    reduced area (d2)
    p1, p2 : (float) pressure measured in free flow (p1), and pressure measured
    after orifice (p2)
    rho : (float) liquid density"""
    pi = 3.141592653589793
    assert p1 > p2, 'Inlet pressure must be greater than low side pressure'
    
    mass_flow = (
            k * (pi/4) * (d2**2) * rho * 
            (2 * (p1-p2) / rho * (1- (d2/d1)**4)) **(1/2)
            )
    
    return mass_flow


if __name__ == '__main__':
    
    
    flow_coeff = 0.6 # [units]
    inlet_pipe_diameter = 0.1 # [meters]
    orifice_pipe_diameter = 0.05 # [meters]
    inlet_pressure = 100000 # pa
    orifice_pressure = 80000 # pa
    density = 1000 # [kg/m^3]
    mass_flow = orifice_mass_flow(flow_coeff,
                                  inlet_pipe_diameter,
                                  orifice_pipe_diameter,
                                  inlet_pressure,
                                  orifice_pressure,
                                  density)
    print("testing orifice_mass_flow")
    print('Calculated Mass Flow : {} \n'.format(mass_flow))
    
    channel_diameter = 8 # [in]
    flow_rate = 640 # [ft^3/min]
    pressure = calculate_velocity_pressure(channel_diameter, flow_rate, box_coef=0.4)
    print('Testing pressure_airflow')
    print('Calculated Pressure : {} \n'.format(pressure))
    
    channel_diameter = 8
    pressure = 0.5
    box_coefficient = 0.45
    airflow = calculate_volumetric_flow(10, 0.03)
    print('Testing velocity_air_flow')
    print('Calculated airflow : {} \n'.format(airflow))

