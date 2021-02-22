#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 09:29:37 2021

@author: anne-laurefrancois
"""


import matplotlib.pyplot as plt
import numpy as np

#%% paramètres

g = 9.81


#%% Initialisation

vitesse = 0
position = 2
temps = 0
temps_chute = np.sqrt((2*position)/g)
increment = temps_chute/50


#%% Méthode d'Euler

fig = plt.figure(figsize = (12, 12))

while temps < temps_chute:
    
    temps = temps + increment
    vitesse = vitesse - g*increment
    position = position + vitesse*increment
    
    ax1 = fig.add_subplot(2,1,1)
    plt.gcf().subplots_adjust(left = 0.1, bottom = 0.1,
                       right = 0.9, top = 0.9, wspace = 0, hspace = 0.2)     
    
    ax1.plot(temps, position,'g+')
    ax1.set_xlabel('temps (s) ')
    ax1.set_ylabel('altitude (m)')
    ax1.set_title('Evolution temporelle de la position')
    
    ax2 = fig.add_subplot(2,1,2) 
    ax2.plot(temps, vitesse, 'bo')  
    ax2.set_xlabel('temps (s) ')
    ax2.set_ylabel('vitesse (m/s)')
    ax2.set_title('Evolution temporelle de la vitesse')
   
   

   

