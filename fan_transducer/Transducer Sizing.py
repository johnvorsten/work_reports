# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:14:47 2019

@author: z003vrzk
"""
import operator
import numpy as np





def calc_flow(orifice_constant, 
              differential_pressure, 
              area, 
              method='standard_density',
              density=0.075):
    """inputs
    -------
    C1 : (float) Orifice inlet constant
    dp : (float) measured differential pressure [inches water column]
    area : Inlet throat area (for fan) @ pressure tap. To use standard density 
    method set area = None [ft^2]
    method : (str) 'standard_density' or 'non_standard_density'. standard 
    density method calculates flow rate given an orifice constant and measured
    differential pressure. Non-standard method is the non-standard air density
    method. It calculates flow rate and corrects differential pressure with
    a measured density.
    density : air density (default 0.075 lb/ft^3). To use Standard Density Method
    set density = None
    output
    -------
    ACMF : Calculated fan flow [ft^3/min]"""
    
    if operator.xor(area, density):
        raise ValueError('Incorrect invocation of airlfow calculation function\
                         set both area and density = None or define')
    
    #Non-standard density method
    if all((bool(area), bool(density), method=='non_standard_density')):
        flow_rate = orifice_constant * area * np.sqrt(differential_pressure/density)
    
    #Standard density method
    elif all((area is None, density is None, method=='standard_density')):
        flow_rate = orifice_constant * np.sqrt(differential_pressure)
        
    else:
        raise ValueError("Incorrect function parameters passed. Check method\
                         argument")
        
    return flow_rate

def calc_dp(flow_rate, C1, area, density=0.075):
    """inputs
    -------
    flow_rate : (float) expected flow rate [ft^3/min]
    C1 : Orifice inlet constant
    area : Inlet throat area (for fan) @ pressure tap. To use standard density method
    set area = None [ft^2]
    density : air density (default 0.075 lb/ft^3). To use Standard Density Method
    set density = None
    output
    -------
    ACMF : Calculated fan flow [ft^3/min]"""
    if operator.xor(bool(area), bool(density)):
        raise ValueError('Incorrect invocation of airlfow calculation function\
                         set both area and density = None or define')
    
    #Non-standard density method
    if all((bool(area), bool(density))):
        dp = ((flow_rate / C1 / area) ** 2) / density
    
    #Standard density method
    if all((area is None, density is None)):
        dp = (flow_rate / C1) ** 2
        
    return dp



if __name__ == '__main__':
    
    #Fan Area
    diameter = 8 #[in]
    area = np.pi*(diameter/2)**2
    
    #Orifice constant
    #From fan manufacturer
    #5.5 HP
    #4 pole 1750 rpm
    #460/3/60
    #diameter 20
    #width 65
    #HPF-A100 wheel
    #88% efficiency motor
    #cone constant 2524
    #cone dp = 6.75 in h20 @ 6632 CFM
    C1 = 2524 #Example
    
    # Minimum expected CFM
    min_cfm = 4200 # [ft^3/min]
    
    #Expected maximum CFM
    max_cfm = 6632 # [ft^3/min]
    
    print('Expected transducer pressure at minimum expected cfm')
    print('calculated dp : ', calc_dp(min_cfm, C1, area=None, density=None))
    
    print('Expected transducer pressure at maximum expected cfm')
    print('calculated dp : ', calc_dp(max_cfm, C1, area=None, density=None))

    







