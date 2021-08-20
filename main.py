# -*- coding: utf-8 -*-
"""
@author: Louis Schirra
"""

import math
import pandas
import random as rd

# Paramètres
decimals = 3
fitness_max = 0.745
max_ind = 5

# Lecture du CSV des data
data = pandas.read_csv("temperature_sample.csv", sep=";")
time = data['#i']
temperature = data['t']

def getBorder(coef):
  if coef == 0:
    border1 = 0
    border2 = 1
  else: 
    border1 = 1
    border2 = 20
  return border1, border2

# Calcul grâce à Weierstrass en fonction de [a, b, c] et du temps
def Weierstrass(individu, time):
  sum = 0
  for n in range(0, individu[2]+1):
    sum = sum + (math.pow(individu[0], n) * math.cos(math.pow(individu[1], n) * math.pi * time))
    
  return sum

# Cumul de l'écart entre Weierstrass et le data_sample en fonction de [a, b, c] à un temps donné
def Fitness(individu):
  cumul = 0

  for i in range(0, len(time)):
    theorique = Weierstrass(individu, time[i])
    delta = abs(theorique - temperature[i])
    cumul = cumul + delta
  
  return round(cumul, decimals)

# Altère aléatoirement a, b ou c
def Mutation(individu):
  result = list.copy(individu)
  param = rd.randint(0, 2)
  value = 0.001 if param == 0 else 1
  
  type_decision = rd.randint(0, 1)
  if type_decision == 1 and (individu[param] - value) > getBorder(param)[0]:
    mut_type = -1
  elif type_decision == 0 and (individu[param] + value) < getBorder(param)[1]:
    mut_type = 1
  else:
    mut_type = 0

  result[param] = round(result[param] + mut_type * value, decimals) if param == 0 else result[param] + mut_type * value

  return result

# Prend la première moitié de individu1 et joint à la deuxième moitié de individu 2 pour créer un nouvel individu
def CrossOver(individu1, individu2):
  new_ind = []
    
  for i in range(0, 2):
      new_ind.append(individu1[i])
  new_ind.append(individu2[2])
  
  return new_ind

# Permet d'obtenir une population de départ avec des fitness convenables
def SelectPop():
    individus = []
    fitnesses = []
    cpt = 0
    
    while cpt < 50:
        for i in range (0, max_ind):
            new_ind = [round(rd.uniform(0.001, 0.999), decimals), rd.randint(1, 20), rd.randint(1, 20)]
            new_fit = Fitness(new_ind)
            if len(individus) < max_ind:
                individus.append(new_ind)
                fitnesses.append(new_fit)
            elif fitnesses[i] > new_fit:
                individus[i] = new_ind
                fitnesses[i] = new_fit
                
        cpt = cpt + 1
    
    return individus

def Algorithme():
  solution = []
  population = SelectPop()
  fitnesses = [Fitness(pop) for pop in population]
  best_fitness = min(fitnesses)
  solution = list(population[fitnesses.index(best_fitness)])
  individus_s = list.copy(population)
  iteration_max = 5000
  supp = 0
  cpt = 0
  
  while cpt < iteration_max and best_fitness > fitness_max:
    decision = rd.randint(1, 2)
    indiv_parent = rd.randint(0, 2)
      
    if decision == 1:
        new_ind = [Mutation(population[indiv_parent]), Mutation(population[indiv_parent])]
        fitnesses.append(Fitness(new_ind[0]))
        fitnesses.append(Fitness(new_ind[1]))
        population.append(new_ind[0])
        population.append(new_ind[1])
    else:
        indiv_parent2 = 0
        while indiv_parent2 == indiv_parent:
            indiv_parent2 = rd.randint(0, 2)
        new_ind = [CrossOver(population[indiv_parent], population[indiv_parent2]),
                   CrossOver(population[indiv_parent], population[indiv_parent2])]
        fitnesses.append(Fitness(new_ind[0]))
        fitnesses.append(Fitness(new_ind[1]))
        population.append(new_ind[0])
        population.append(new_ind[1])
    
    # Supprime 2 pires puis recrée 2 par mutation/crossover
    for i in range(0, 2):
        del population[fitnesses.index(max(fitnesses))]
        del fitnesses[fitnesses.index(max(fitnesses))]

    best_fitness = min(fitnesses)
    solution = list(population[fitnesses.index(best_fitness)])
    cpt = cpt + 1
  
  print("Valeurs initiales : ", individus_s ,
        "\nValeur trouvée : ", solution, 
        "\nMeilleure fitness trouvée : ", best_fitness, 
        "\nNombre d'itérations : ", cpt)

Algorithme()