# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 09:43:36 2020

Reference
https://www.engproguides.com/heatequations.html


@author: z003vrzk
"""

# Python
import math

# Third party

# Local imports

#%% Coil Sizing

def log_mean_temperature_difference(process_in, process_out,
                                    regen_in, regen_out):
    """Log mean temperature difference
    inputs
    -------
    process_in
    process_out
    regen_in
    regen_out : (float)"""

    ta = math.fabs(process_in - regen_in)
    tb = math.fabs(process_out - regen_out)
    lmtd = (ta - tb) / math.log((ta / tb), math.e)

    return lmtd

def heat_transfer_coil(heat_transfer_coefficient,
                       area,
                       temperature_in,
                       temperature_out):
    """
    inputs
    -------
    outputs
    -------"""
    return heat_transfer_coefficient * area * (temperature_out - temperature_in)


if __name__ == '__main__':
    process_in = 90
    process_out = 55
    regen_in = 44
    regen_out = 56

    # Log mean temperature difference
    lmtd = log_mean_temperature_difference(process_in,
                                           process_out,
                                           regen_in,
                                           regen_out)



#%%
"""Calculate energy usage of a typical shower"""

def internal_energy(cp, tin, tout, mass):
    """Calculate energy of temperature change of a mass
    inputs
    -------
    cp : (float) heat capacity coefficient, constant pressure
    tin : (float) temperature into process [units depend on cp]
    tout : (float) temperature out of process [units depend on cp]
    mass : (float) mass (or mass flow rate) [units depend on cp]
    output
    -------
    energy : (float) energy or energy rate [units depend on cp, tin, tout,
            mass]

    Conservation of energy, constant pressure enregy transfer
    Total energy
    m Mass, [lb,kg]
    m_dot mass flow rate [lbm/h, Kg/s]
    h enthalpy [BTU/(h*F), KJ/(Kg*K)]
    Q total energy [Btu, KJ]
    q energy time rate [Btu/h, W, J/s]
    cp heat capacity at constant pressure [KJ/(Kg*K), BTU/(lbm*T)]

    Q = m * h
    q = m_dot * h
    q1 - q2 = m_dot * (h1 - h2) = m_dot * cp * (t1 - t2)
    q = m_dot * (h1 - h2) = rho * V * A * (h1 - h2)
    q = rho * cp * volumetric_flow * (t1 - t2)"""
    return cp * mass * (tout - tin)


def output_temperature_energy_conservation(energy, cp, tin, mass):
    """Calculate energy of temperature change of a mass
    inputs
    -------
    cp : (float) heat capacity coefficient, constant pressure
    tin : (float) temperature into process [units depend on cp]
    energy : (float) energy or energy rate [units depend on cp, tin, tout,
            mass]
    mass : (float) mass (or mass flow rate) [units depend on cp]
    output
    -------
    tout : (float) temperature out of process [units depend on cp]

    Conservation of energy, constant pressure enregy transfer"""

    tout = (energy) / (cp * mass) + tin

    return tout


def internal_energy(cp, tin, tout, mass):
    """Calculate energy of temperature change of a mass
    inputs
    -------
    cp : (float) heat capacity coefficient, constant pressure
    tin : (float) temperature into process [units depend on cp]
    tout : (float) temperature out of process [units depend on cp]
    mass : (float) mass (or mass flow rate) [units depend on cp]
    output
    -------
    energy : (float)"""
    return cp * mass * (tout - tin)

def farenheit2celsius(degf):
    return (degf - 32) * (5 / 9)

def gallon2cubicmeter(gallons):
    return 0.0037854118 * gallons

#%%


if __name__ == '__main__':

    #%% Calculate energy usage of shower
    # Specific heat
    cp = 4.187 # kJ/kgK = 1.001 Btu(IT)/(lbm °F) or kcal/(kg K)
    # Elapsed time with water flowing
    dt = 6 # minutes
    tin = 70 # degrees Farenheit
    tout = 100 # Degrees Farenheit
    water_density = 992.25 # kg/m3 at 40 Deg C
    flow = 2.1 # gallons / minute
    energy_cost_rate = 0.13 # dollars / kWh
    water_cost_rate = 10 / 1000 # dollars / gallon

    # Calculate total water usage, [kg]
    gal = dt * flow # gallons
    kg = gallon2cubicmeter(gal) * water_density # kg

    # Calculate energy usage
    energy = internal_energy(cp, tin, tout, kg) # kJ
    kwh = energy * (1/60) * (1/60) # kWh
    value = kwh * energy_cost_rate # dollars

    # Console
    print("Total energy usage : {:.2f} [kWh]".format(kwh))
    print("Total water usage : {:.1f} [gal]".format(gal))
    print("Total cost : {:.2f} [USD]".format(value))
    print("Rate cost : {:.2f} [USD/min]".format(value / dt))

    #%% Output temperature of constant airflow heat transfer
    cp = 1.008 # Combined density and heat capacity of air at SI conditions
    tin = 55 # [DEG F]
    tout = None # [DEG F]
    energy = 16 * 1000 # [mmBTU*h]
    flow = 425 # [ft^3 / minute]

    tout = output_temperature_energy_conservation(energy, cp, tin, flow)
    msg = ("Output airflow temperature {:0.2f} [DEG F] at {} [ft^3/min], {} [DEG F] inlet," +
        " {:.1f} [mmBTU] heat transfer")
    print(msg.format(tout, flow, tin, energy/1000))

