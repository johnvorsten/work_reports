# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 13:40:33 2019

@author: z003vrzk
"""




"""
#%% General enthalpy of water

Energy change be calculated based on internal energy.
Internal enregy of water is calculated using the enthalpy of water
at different temperatures

H = U + PV
enthalpy = (Internal energy) + (pressure * Volume)

Assuming water stays in the liquid phase, the chagnge of enthalpy can be 
simplified to 

H = U

internal energy = specific heat * mass * (temperature2 - temperature1)

If temperature 1 is taken to be 0 kelvin, then the enthalpy at temperature 2 
should be equivalent to the interal energy at temperature 2 (This assumes 
no pressure boundary work between phase changes of the material).  In general
this is a bad assumption.  BUT this lets us write

h = cp * (temp2 - temp1)

Use gas, steam, and other matter tables for better estimates


#%% General thermodynamics, total energy equation

0 = m(hin + (vin/2) ** 2 + zin) = m(hout, (vout/2)**2 + zout)






"""


def constant_flow_heat_rate(t1, t2, flow_rate, media='water', units='ip'):
  """
  Calculate the heat rate (power) transferred from air or water
  given a temperature differentiala nd flow rate
  inputs
  -------
  t1 : (float) Inlet fluid temperature
  t2 : (float) outlet fluid temperature
  flow : (float) flow rate of fluid. Must be [cfm] for air, and [gpm] for water
  if units=='ip', or [L/s] for air and [kg/s] for water if units=='si'
  units : (str) 'si' for standard international (metric) or 'ip' for imperial
  media : (str) 'water' or 'air'
  """
  if all((media=='air',units=='ip')):
    conversion_constant = 1.08
  elif all((media=='air',units=='si')):
    conversion_constant = 1.2
  if all((media=='water',units=='ip')):
    conversion_constant = 500
  if all((media=='water',units=='si')):
    conversion_constant = 4180
    
  power = conversion_constant * flow_rate * (t2 - t1)
  
  return power


def constant_flow_flow_rate(t1, t2, heat_rate, media='water', units='ip'):
  """
  Calculate the heat rate (power) transferred from air or water
  given a temperature differentiala nd flow rate
  inputs
  -------
  t1 : (float) Inlet fluid temperature, DEG F if units=='ip', or DEG C if 
  units=='si'
  t2 : (float) outlet fluid temperature, DEG F if units=='ip', or DEG C if 
  units=='si'
  flow : (float) flow rate of fluid. Must be [cfm] for air, and [gpm] for water
  if units=='ip', or [L/s] for air and [kg/s] for water if units=='si'
  units : (str) 'si' for standard international (metric) or 'ip' for imperial
  media : (str) 'water' or 'air'
  """
  if all((media=='air',units=='ip')):
    conversion_constant = 1.08
  elif all((media=='air',units=='si')):
    conversion_constant = 1.2
  if all((media=='water',units=='ip')):
    conversion_constant = 500
  if all((media=='water',units=='si')):
    conversion_constant = 4180
    
  flow_rate = heat_rate / conversion_constant / (t2 - t1)
  
  return flow_rate

if __name__ == '__main__':
  
  # Hot water coil
  # Assume 20 degree delta temperature
  hot_temperature_in = 180 # degrees F
  hot_temperature_out = 160 # degrees F
  hot_power = 244945 # Btu/hr
  
  # Chilled water coil
  # Assume 14 degree delta temperature
  cold_temperature_in = 45
  cold_temperature_out = 59
  cold_power = 302262 # Btu/hr
  
  flow_hot = constant_flow_flow_rate(hot_temperature_in, 
                                     hot_temperature_out, 
                                     hot_power)
  print('Hot water flow calculated : {}'.format(flow_hot))

  flow_cold = constant_flow_flow_rate(cold_temperature_in, 
                                      cold_temperature_out, 
                                      cold_power)
  print('Cold water flow calculated : {}'.format(flow_cold))
