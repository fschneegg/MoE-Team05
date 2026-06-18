import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = r'Masterstudium\Modellierung von Energiesystemen\Lastprofil mittelgroßes Krankenhaus.csv'

lp = pd.read_csv(path, sep = ';')

lp['timestamp_UTC'] = pd.to_datetime(lp['timestamp_UTC'], errors='coerce')
lp = lp.dropna(subset=['timestamp_UTC'])

lp['load[kW]'] = lp['load[kW]'].str.replace(',', '.', regex=False)
lp['load[kW]'] = pd.to_numeric(lp['load[kW]'])

print('Maximal:', lp['load[kW]'].max(),'\n'
    'Minimal:', lp['load[kW]'].min(),'\n'
    'Durschnitt:', lp['load[kW]'].mean())

