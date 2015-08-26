# -*- coding: cp1252 -*-
#Universidad del Valle de Guatemala
#Algoritmos y Estructuras de Datos
#Sección 10
#
#Hoja de Trabajo 5
#
#SimOS.py
#
#Jorge Manrique
#   13600
#
#Christopher Ajú
#   13171
#

#imports
import simpy
import random

#variables


#Cuerpo de programa
#Titulo de inicio
print ("Simulacion de corrida de programas en un Sistema Operativo de tiempo compartido.")

#Objeto proceso
class Proceso(object):
    def __init__(self, name, tasks, env):
        print ("inicio del proceso")
        
#se crea el ambiente de simulacion
env = simpy.Environment()

#se crea el resource
#new: lista para los nuevos procesos

#ready: lista de procesos en espera a ser atendidos

#running: procesos en ejecucion

#waiting: procesos en espera


