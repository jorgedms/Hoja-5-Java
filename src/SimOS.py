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
import time
import math
#from SimOS1 import promedio

#DATOS GENERALES
#semilla para generar los mismos numeros para las simulaciones
random.seed(42)
#la cantidad de procesos a generar
numProcesos = 200
intervalo = 3.0
#cantidad de ram
global cantRam 
cantRam= 100
#cantidad de instrucciones por unidad de tiempo: 3 unidades de tiempo en espera
global cpuMax 
cpuMax= 3
#la cantidad de procesadores de la maquina
#global cantProcesadores
cantProcesadores = 1
#cantidad de instrucciones del proceso
#global instructions 
#instructions = random.randint(1, 11)
#cantidad de ram requerida por proceso
#global ramNeed
#ramNeed = random.randrange(1, 11)




#la clase proceso
def proceso (env, nombre, cpu, ram, wait, ramNeed, instrucciones):
    #seccion new del diagrama
    #almacenaje del momento de creacion
    global tiempo_total
    time_cero = env.now
    #impresion del tiempo 0
    print ('proceso %s se creo en el tiempo %s' %(nombre,time_cero))
    
    #solicitud de ram
    yield ram.get(ramNeed)
    #al finalizar el yield se ingresa a la seccion ready y running
    #time1 = tiempo en el que se incia a ejecutar el proceso
    time_uno = env.now
    print ('Proceso %s enviado a ready en el tiempo: %s con %s instrucciones vigentes' %(nombre, time_uno, instrucciones))
        
    #ciclo para realizar todos los procesos 
    while (instrucciones>0):
        print ('entrada de while')
        print ('Proceso %s con %s instrucciones' %(nombre, instrucciones))
        #se solicita el recurso de cpu, o entrada a running
        with cpu.request() as request:
            yield request
            #se almacena el tiempo de ingreso al cpu
            time_dos = env.now
            #se imprime el tiempo de ingreso a running
            #print ('Proceso %s ingreso al CPU en el tiempo %s con %s instrucciones vigentes' %(nombre, time_dos, instrucciones))
       
            #se esperan las unidades de tiempo por proceso 
            #se puede implementar un ciclo de espera de 1 unidad de tiempo 
            #para tener un tiempo mas exacto por proceso
            yield env.timeout(cpuMax)
            instrucciones = instrucciones -3
            time_tres = env.now
            print ('Proceso %s sale de running en el tiempo: %s con %s instrucciones vigentes' %(nombre, time_tres, instrucciones))
            #se resta 3 procesos al total de procesos necesarios
            #instrucciones = instrucciones - 3
        
            #comparacion if para verificar si se finalizo el proceso
            if ((instrucciones)<=0):
                #se deja el proceso en 0
                #instrucciones = 0
                #se calcula el tiempo tomado
                timeAll = (env.now) - time_cero
                #se agrega al tiempo que requirieron los demas procesos
                tiempo_total = tiempo_total + timeAll
                #print ('Tiempo total: %s' %tiempo_total)
                print ('Proceso %s le llevo %s unidades de tiempo para terminar<-----------------------------------------------------fin de proceso' %(nombre, timeAll))
                print ('\n\n')
                #se devuelve la cantidad de memoria ram usada por el proceso
                ram.put(ramNeed)
            #se envia el proceso a waiting o a ready
            else:
                #instrucciones = instrucciones - 3
                sendTo = random.randint(1,2)
                print ('El random: %s' %sendTo)
                #if que envia el proceso a wainting si el valor generado es 1
                if sendTo == 1:
                    #with wait.request() as request2:
                    yield wait.request()
                    time_cuatro = env.now
                    print ('Proceso %s en cola de waiting en el tiempo %s' %(nombre, time_cuatro))
                    #1.  se espera en la seccion wait una cantidad random de tiempo porque
                    #    se simula un ingreso de usuario
                    #2. ya que no se especifica cuanto tiempo puede estar en waiting se 
                    #   toma un ciclo del procesador como tiempo maximo
                    yield env.timeout((random.randint(1,cpuMax)))
                    #se almacena el tiempo de salida
                    time_cinco = env.now
                    #se imprime la salida de la cola waiting
                    print ('Proceso %s ha terminado de esperar ingreso de usuario en el tiempo %s' %(nombre, time_cinco ))
                #no se realiza el envio a ready ya que esta el ciclo while en el inicio del codigo
                else:
                    print ('no se envio a waiting')
    #fin del while: no hay mas procesos
                print ('fin del while de proceso %s' %nombre)

#clase para generar todos los objetos proceso
def generador (env, numProcesos,intervalo,cpu,wait,ram):
        #ciclo para generar la cantidad especificada de procesos en variable
        for i in range(numProcesos):
            ramNeed = random.randint(1, 10)
            instrucciones = random.randint(1, 10)
            newProceso = proceso(env, 'No.%s' %i, cpu, ram, wait, ramNeed, instrucciones)
            env.process(newProceso)
            delay = random.expovariate(1.0/intervalo)
            yield env.timeout(delay)

#DATOS DE AMBIENTE DE SIMULACION
#se crea el ambiente de simulacion
env = simpy.Environment()
#se crea el contenedor de ram
ram = simpy.Container(env, cantRam, init=cantRam)
#se crea el procesador
#global cpu
cpu = simpy.Resource(env, capacity=1)
#se crea la seccion waiting
wait = simpy.Resource(env, capacity=1)
#inicio de simulacion

#DATOS DE PROCESOS
global tiempo_total
tiempo_total = 0


env.process(generador(env, numProcesos, intervalo, cpu, wait, ram))
env.run()   

global promedio
promedio = (tiempo_total/numProcesos)

#impresion de los datos para graficas
print ('Tiempo total: %s' %tiempo_total)
print ('Promedio de tiempo: %s' %promedio)
