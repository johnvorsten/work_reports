# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:46:56 2019

@author: z003vrzk
"""

"""
Equations of state

y_space_supply = 0.87 * y_supply

y_space_exhaust = y_exhaust

# Enforce
y_space_supply - y_space_exhaust = 0
y_space_supply * 0.87 = y_space_exhaust

# Controller parameters
transferred_air = y_supply - y_exhaust
transferred_air_setpoint = 0

"""

# Third party imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapz



#%% 


# Variables
_N_POINTS = 100
_Y_SUPPLY_MAX = 395
_Y_SUPPLY_MIN = 120
_Y_SUPPLY = np.linspace(start=_Y_SUPPLY_MIN, 
                        stop=_Y_SUPPLY_MAX, 
                        num=_N_POINTS) # Scheduled airflow
_Y_EXHAUST_MAX = 345
_Y_EXHAUST_MIN = 130 # Not actual, but just pretend
_Y_EXHAUST = np.linspace(start=_Y_EXHAUST_MIN, 
                         stop=_Y_EXHAUST_MAX, 
                         num=_N_POINTS)

_TRANSFERRED_AIR_SETPOINT = 0
_Y_EXHAUST_SIMULATED = 35.5

# Simulation and graphing

# Calculate steady state error at all airflows
# Transferred air as calculated from the terminal unit, no additional exhaust simulated
# This is synonymous with error
transferred_air_controller_case1 = _Y_SUPPLY - _Y_EXHAUST
# Transferred air as calculated from terminal unit, additional exhaust simulated
transferred_air_controller_case2 = _Y_SUPPLY - _Y_EXHAUST - _Y_EXHAUST_SIMULATED

# Assume the controller drives error to zero by increasing supply
# These are actual supply and exhaust measured at terminal unit
y_supply_case1 = _Y_EXHAUST - _TRANSFERRED_AIR_SETPOINT
y_space_supply_case1 = 0.87 * y_supply_case1
y_supply_case2 = _Y_EXHAUST - _TRANSFERRED_AIR_SETPOINT + _Y_EXHAUST_SIMULATED
y_space_supply_case2 = 0.87 * y_supply_case2

# Calculate space transferred air
y_space_transferred_air_case1 = y_space_supply_case1 - _Y_EXHAUST
y_space_transferred_air_case2 = y_space_supply_case2 - _Y_EXHAUST

error_case1 = trapz(abs(y_space_transferred_air_case1))
error_case2 = trapz(abs(y_space_transferred_air_case2))

print('Error case 1 : {}'.format(error_case1))
print('Error case 2 : {}'.format(error_case2))


#%% Plotting

# Plot over/underpressurization on the y axis
# plot cfm on the x axis
fig, ax = plt.subplots(1)
ax.plot(np.arange(0,_N_POINTS,1), _Y_SUPPLY, lw=2, label='Supply air (cfm)')
ax.plot(np.arange(0,_N_POINTS,1), _Y_EXHAUST, lw=2, label='exhaust air (cfm)')
ax.plot(np.arange(0,_N_POINTS,1), y_space_transferred_air_case1, lw=2, label='C115R1 transferred air case1 (cfm)')
ax.plot(np.arange(0,_N_POINTS,1), y_space_transferred_air_case2, lw=2, label='C115R1 transferred air case2 (cfm)')
ax.plot(np.arange(0,_N_POINTS,1), transferred_air_controller_case1, lw=2, label='Error @ TU case1 (cfm)')
ax.plot(np.arange(0,_N_POINTS,1), transferred_air_controller_case2, lw=2, label='Error @ TU case2 (cfm)')


ax.set_ylabel('Airflow (CFM)')
ax.set_title('Lab C155R1 airflow')
ax.set_xlim(left=0)
ax.grid(True)
ax.legend()


#%% Minimization and root finding

from scipy.optimize import minimize
from scipy.optimize import LinearConstraint
from scipy.integrate import trapz

# Create the function

def integrated_error(x, *args):
    """Function to be minimized"""
    
    # Variables
    _N_POINTS = 100
    _Y_SUPPLY_MAX = args[0]
    _Y_SUPPLY_MIN = args[1]
    _Y_SUPPLY = np.linspace(start=_Y_SUPPLY_MIN, 
                            stop=_Y_SUPPLY_MAX, 
                            num=_N_POINTS) # Scheduled airflow
    _Y_EXHAUST_MAX = args[2]
    _Y_EXHAUST_MIN = x[1] # Not actual, but just pretend
    _Y_EXHAUST = np.linspace(start=_Y_EXHAUST_MIN, 
                             stop=_Y_EXHAUST_MAX, 
                             num=_N_POINTS)
    
    _TRANSFERRED_AIR_SETPOINT = 0
    _Y_EXHAUST_SIMULATED = x[0]
    
    # Simulation and graphing
    
    # Calculate steady state error at all airflows
    # This is synonymous with error
    # Transferred air as calculated from terminal unit, additional exhaust simulated
    transferred_air_controller_case2 = _Y_SUPPLY - _Y_EXHAUST - _Y_EXHAUST_SIMULATED
    
    # Assume the controller drives error to zero by increasing supply
    # These are actual supply and exhaust measured at terminal unit
    y_supply_case2 = _Y_EXHAUST - _TRANSFERRED_AIR_SETPOINT + _Y_EXHAUST_SIMULATED
    y_space_supply_case2 = 0.87 * y_supply_case2
    
    # Calculate space transferred air
    y_space_transferred_air_case2 = y_space_supply_case2 - _Y_EXHAUST
    
    # Integrate space transferred air to get total error over evaluation interval
    error_integral = trapz(abs(y_space_transferred_air_case2))
    
    return error_integral

_Y_SUPPLY_MAX = 395
_Y_SUPPLY_MIN = 120
_Y_EXHAUST_MAX = 345
args = (_Y_SUPPLY_MAX, _Y_SUPPLY_MIN, _Y_EXHAUST_MAX)

# Must apply constraint that supply_flow * 0.87 = exhaust_flow..
constraint_list = [{'type':'eq', 'fun':lambda x: x[1] - _Y_SUPPLY_MIN*0.87}]

_Y_EXHAUST_SIMULATED0 = 25
_Y_EXHAUST_MIN0 = 104
x0 = np.array([_Y_EXHAUST_SIMULATED0, _Y_EXHAUST_MIN])
res = minimize(integrated_error, 
               x0, 
               constraints=constraint_list,
               args=args, 
               method='SLSQP', 
               bounds=[(0,50), (100,130)])

