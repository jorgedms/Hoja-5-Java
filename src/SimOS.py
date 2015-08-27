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

#DATOS GENERALES
#semilla para generar los mismos numeros para las simulaciones
random.seed(9)
#la cantidad de procesos a generar
numProcesos = 25
#cantidad de ram
global cantRam 
cantRam= 100
#cantidad de instrucciones por unidad de tiempo: 3 unidades de tiempo en espera
global cpuMax 
cpuMax= 3
#cantidad de instrucciones del proceso
global instructions 
#instructions = random.randint(1, 11)
#cantidad de ram requerida por proceso
global ramNeed
#ramNeed = random.randrange(1, 11)

#DATOS DE PROCESOS
global Tiempot
Tiempot = 0

#DATOS DE AMBIENTE DE SIMULACION
#se crea el ambiente de simulacion
env = simpy.Environment()
#se crea el contenedor de ram
ram = simpy.Container(env, cantRam, cantRam)
#se crea el procesador
cpu = simpy.Resource(env, capacity=1)
#se crea la seccion waiting
wait = simpy.Resource(env, capacity=1)
#verificacion de datos
#se puede eliminar, solo sirvio para verificar
for i in range(numProcesos):
    ramNeed = random.randint(1, 10)
    instrucciones = random.randint(1, 10)
    print ('Proceso %s con valor de Ram %s y %s instrucciones' %(i, ramNeed, instrucciones))
    x = random.randint(1,2)
    print ('valor random generado: %s' %(x))
    
#def source


#la clase proceso
def proceso (env, nombre, ramNeed,instrucciones):
    #seccion new del diagrama
    #almacenaje del momento de creacion
    time0 = env.now()
    #impresion del tiempo 0
    print ('proceso %s se creo en el tiempo %s' %(nombre,time0))
    
    #solicitud de ram
    yield ram.get(ramNeed)
    #al finalizar el yield se ingresa a la seccion ready y running
    #time1 = tiempo en el que se incia a ejecutar el proceso
    time1 = env.now
    print ('Proceso %s enviado a ready en el tiempo: %s' %(nombre, time1))
        
    #ciclo para realizar todos los procesos 
    while (instrucciones>0):
        #se solicita el recurso de cpu, o entrada a running
        yield cpu.request()
        #se almacena el tiempo de ingreso al cpu
        time2 = env.now
        #se imprime el tiempo de ingreso a running
        print ('Proceso %s ingreso al CPU en el tiempo %s' %(nombre, time2))
       
        #se esperan las unidades de tiempo por proceso 
        #se puede implementar un ciclo de espera de 1 unidad de tiempo 
        #para tener un tiempo mas exacto por proceso
        yield env.timeout(cpuMax)
        time3 = env.now
        print ('Proceso %s sale de running en el tiempo: %s' %(nombre, time3))
        #se resta 3 procesos al total de procesos necesarios
        instrucciones = instrucciones - 3
        
        #comparacion if para verificar si se finalizo el proceso
        if (instrucciones<=0):
            #se deja el proceso en 0
            instrucciones = 0
            #se calcula el tiempo tomado
            timeAll = (env.now) - time0
            #se agrega al tiempo que requirieron los demas procesos
            tiempot = Tiempot + timeAll
            print ('Proceso %s le llevo %s unidades de tiempo para terminar' %(nombre, timeAll))
            #se devuelve la cantidad de memoria ram usada por el proceso
            ram.put(ramNeed)
        #se envia el proceso a waiting o a ready
        else:
            sendTo = random.randint(1,2)
            #if que envia el proceso a wainting si el valor generado es 1
            if sendTo == 1:
                yield wait
                time4 = env.now
                print ('Proceso %s en cola de waiting en el tiempo %s' %(nombre, time4))
                #1.  se espera en la seccion wait una cantidad random de tiempo porque
                #    se simula un ingreso de usuario
                #2. ya que no se especifica cuanto tiempo puede estar en waiting se 
                #   toma un ciclo del procesador como tiempo maximo
                yield env.timeout((random.randint(1,cpuMax)))
                #se almacena el tiempo de salida
                time5 = env.now
                #se imprime la salida de la cola waiting
                print ('Proceso %s ha terminado de esperar ingreso de usuario en el tiempo %s' %(nombre, time5 ))
            #no se realiza el envio a ready ya que esta el ciclo while en el inicio del codigo
    #fin del while: no hay mas procesos



    