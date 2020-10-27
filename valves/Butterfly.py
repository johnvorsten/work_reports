# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 12:44:44 2020

Calculate required actuator torque on butterfly valves

There are a number of torques which butterfly valves may
experience such as:

Tsu - Seating and Unseating Torque
The seating/unseating torque value (Tsu) is a function of the
pressure differential, the seat material’s coefficient of friction,
the finished surface of the disc edge, the amount of interference
between the seat I.D. and disc O.D. when flanged in piping, the
seat thickness, and the type of service (media) for which the valve
is being used

Td - Dynamic Torque Resulting from fluid flow

Tbf – Bearing Friction Torque

Tss – Stem Seal Friction Torque
For all practical purposes stem seal friction torque values are
insignificant when compared to seating/unseating and bearing
friction torques

Te – Eccentricity Torque resulting from disc offset from 
centerline of stem (either single,
double or triple offset)

Th – Hydrostatic Torque
We will ignore discussion of the hydrostatic torque values as they
are generally insignificant compared to the seating/unseating, 

@author: z003vrzk
"""

# Seating / unseating values
# Class B - general sevice only



def get_torque_bfv(valve_diameter,
                   shaft_diameter, 
                   pressure_differential):
    """Description
    Inputs
    -------
    valve_diameter : (float) units of inch, diameter of valve disc
    shaft_diameter : (float) units of inch, diameter of valve shaft
    pressure_differential : (float) units of psi, pressure across closed valve
    """
    
    # Assumptions, initial values
    # Coefficient of friction
    cf = 0.25
    
    # Calculate hydrostatic torque
    Th = 0
    
    # Calculate stem seal friction toruqe
    Tss = 0
    
    # Bearing friction torque
    Tbf = 0.785 * cf * valve_diameter ** 2 * (shaft_diameter / pressure_differential)
    
    # Seating / unseating force
    Tsu = 
    
    torque_required = Th + Tbf + 
    
    pass