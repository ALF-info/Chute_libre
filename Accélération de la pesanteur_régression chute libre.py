#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 11:17:11 2021

@author: anne-laurefrancois
"""


import numpy as np
from matplotlib import pyplot as plt

#%% Définition du tirage au sort de la valeur d'une variable

"""
    Renvoie une valeur x aléatoire de la variable X d'incertitude-type u(X)
        X = [x, u(X)] (loi normale)
"""

def Alea(X):
    tirage = np.random.normal()   
    return X[0]+X[1]*tirage

#%% Procedure Regression Linéaire; tableaux np X et Y (méthode des moindres carrés)
    
def RegLin(X,Y):
    N = len(X)
    moyX = sum(X)/N
    moyY = sum(Y)/N
    pente = sum((X-moyX)*(Y-moyY))/(sum((X-moyX)**2))   # calcule la pente de la droite de régression
    ordor = moyY - pente*moyX                           # calcule l'ordonnée à l'origine de la droite de régression
    return [pente,ordor]

#%% Entrées
    
hauteur_chute = [0.600,0.550,0.500, 0.450,0.400]        # Liste contenant les hauteurs de chute (m)
duree_chute = [0.350,0.335,0.319,0.303,0.286]           # Liste contenant les durées de chute (s)
incertitude_duree_chute =  1e-3                         # Estimation de l'incertitude-type sur la durée de chute (s) 
incertitude_hauteur_chute = 1e-3                        # Estimation de l'incertitude-type sur la hauteur de chute (m)                       
                                                      


#%% Préparation des listes avec incertitudes

Hauteur_chute = []
for k in range(len(hauteur_chute)):
    Hauteur_chute.append([hauteur_chute[k], incertitude_hauteur_chute])            # Remplit une liste de listes contenant les hauteurs de chute assorties de leur incertitude 
    
Duree_chute = []
for k in range(len(duree_chute)):
    Duree_chute.append([(duree_chute[k]), incertitude_duree_chute])           # Remplit une liste de listes contenant les durées de chute assorties de leur incertitude 
    
#%% Méthode de Monte Carlo pour déterminer les incertitudes sur la pente et l'ordonnée à l'origine de la régression linéaire
    
LPente = []     # Crée une liste vide pour stocker les valeurs de la pente de la droite de régression issues de la simulation
LOrdor = []     # Crée une liste vide pour stocker les valeurs de l'ordonnée à l'origine de la droite de régression issues de la simulation

iterations = 100000     # Nombre d'essais de la simulation

for i in range(iterations):
    

    Alea_hauteur_chute = []          # Crée une liste vide pour stocker les valeurs de la hauteur de chute issues de la simulation
    Alea_duree_chute = []            # Crée une liste vide pour stocker les valeurs de la durée de chute issues de la simulation
    
    for k in range(len(hauteur_chute)):
       
        Alea_hauteur_chute.append(Alea(Hauteur_chute[k]))                                   # Remplit la liste  Alea_hauteur_chute avec des valeurs tirées au hasard (loi normale) de la hauteur de chute
        Alea_duree_chute.append(Alea(Duree_chute[k])**2)                                    # Remplit la liste  Alea_duree_chute avec des valeurs tirées au hasard (loi normale) du carré de la durée de chute
    Pente = RegLin(np.array(Alea_duree_chute),np.array(Alea_hauteur_chute))[0]              # Calcule la pente de la droite de régression pour chaque itération
    OrdOr = RegLin(np.array(Alea_duree_chute),np.array(Alea_hauteur_chute))[1]              # Calcule l'ordonnée à l'origine de la droite de régression pour chaque itération
    LPente.append(Pente)                                                                    # Remplit la liste LPente avec les valeurs calculées de la pente de la droite de régression pour chaque itération
    LOrdor.append(OrdOr)                                                                    # Remplit la liste LOrdor avec les valeurs calculées de l'ordonnée à l'origine de la droite de régression pour chaque itération
    
MoyPente = np.sum(LPente)/iterations                                                        # Calcule la moyenne des valeurs simulées de la pente 
MoyOrdOr = np.sum(LOrdor)/iterations                                                        # Calcule la moyenne des valeurs simulées de l'ordonnée à l'origine

incertitude_type_Pente = np.std(np.array(LPente))                                           # Calcule l'incertitude-type sur la pente de la droite de régression
incertitude_elargie_Pente = 2*incertitude_type_Pente                                        # Calcule l'incertitude élargie sur la pente de la droite de régression
incertitude_type_OrdOr = np.std(np.array(LOrdor))                                           # Calcule l'incertitude-type sur l'ordonnée à l'origine de la droite de régression
incertitude_elargie_OrdOr = 2*incertitude_type_OrdOr                                        # Calcule l'incertitude élargie sur l'ordonnée à l'origine de la droite de régression

#%% Affichage

print ('Pente de la droite de régression:', MoyPente, 'm/s^2')
print('Incertitude élargie sur la pente :',incertitude_elargie_Pente, 'm/s^2')
print("Ordonnée à l origine :",MoyOrdOr, 'm')
print("Incertitude élargie sur l'ordonnée à l origine:",incertitude_elargie_OrdOr, 'm')

fig = plt.figure(figsize = (10, 10))                                                        # Crée une zone graphique
plt.gcf().subplots_adjust(left = 0.1, bottom = 0.1,
                       right = 0.9, top = 0.9, wspace = 0, hspace = 0.2)                    # Ajuste les valeurs des marges de la figure
ax1 = fig.add_subplot(2,1,1)                                                                # Crée le premier graphe de la figure
ax1.hist(LPente, range = (4, 6), bins = 50, color = 'orange', edgecolor = 'black')        # Affiche l'histogramme de répartion des valeurs simulées de la pente
ax1.set_xlabel('Pente (m/s^2) ')
ax1.set_ylabel('effectif')
ax1.set_title('Pour 100 000 iterations')

ax2 = fig.add_subplot(2,1,2)                                                                # Crée le deuxième graphe de la figure
ax2.hist(LOrdor, range = (-0.1, 0.1), bins = 50, color = 'blue', edgecolor = 'black')       # Affiche l'histogramme de répartion des valeurs simulées de l'ordonnée à l'origine
ax2.set_xlabel("Ordonnée à l'origine (m)")
ax2.set_ylabel('effectif')


plt.show()    


