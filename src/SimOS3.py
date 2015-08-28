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
import math
from math import sqrt

def proceso(nombre,total_instrucciones,total_ram,delay,work):
    global tiempo_final
    global desviacion_estandar
    tiempo_inicio = 0
    
    #seccion new del diagrama
    #delay de entrada
    yield env.timeout(delay)
    
    #ciclo while para mantener en el cpu
    #la comparacion cumple con el requisito de ser mayor que el ciclo de trabajo
    #si no cumple se libera el cpu
    while(total_instrucciones>work):
        #seccion admitted del diagrama
        #se solicita ram
        yield ram.get(total_ram)
        #seccion ready del diagrama
        tiempo_inicio = env.now
        #se imprime el tiempo de ingreso, cantidad de procesos y ram requerida
        print ('Proceso No.%s: ingreso en:%s con: %s procesos y %s de ram' %(nombre, tiempo_inicio, total_instrucciones,total_ram))
        #se imprime la cantidad de ram restante
        print ('RAM restante: %s' %ram.level)
        #seccion running del diagrama
        with cpu.request() as request:
            yield request
            #ciclo de 3 unidades de tiempo = variable work
            #flag = lleva el conteo de ciclos realizados
            #se inicia flag
            flag = 0
            while (flag!=work):
                #se elimina una instruccion
                print ('checkpoint')
                total_instrucciones=total_instrucciones-1
                print('Instrucciones restantes de proceso No.%s: %s' %(nombre,total_instrucciones))
                #se espera la unidad de tiempo
                yield env.timeout(1)
                #se suma 1 a flag
                flag = flag + 1
        #se realiza el random para saber si se envia a waiting o a ready
        #1 = waiting; 2= ready
        send = random.randint(1,2)
        if(send==1):
            with wait.request() as request_wait:
                #se espera hasta tener acceso al wait
                yield request_wait
                #se simula un ingreso de usuario
                print ('espera a ingreso de informacion')
                yield env.timeout(3)
                print ('usuario ha ingresado informacion')
        #seccion terminated del diagrama
        yield ram.put(total_ram)
        end = ((env.now)-tiempo_inicio)
        #se almacena el tiempo total de proceso y se suma a los otros
        tiempo_final = tiempo_final+end
        #se imprime el tiempo que se tomo en finalizar la tarea
        print ('Proceso No.%s finalizado en %s unidades de tiempo\n\n' %(nombre,end))
        #elevar cada tiempo al cuadrado  y sumarlo con los otros tiempos
        desviacion_estandar = (desviacion_estandar+(tiempo_final**2))
        
#variables a cambiar para las simulaciones
random.seed(9)
cpu_cant = 1 #cantidad de procesadores
ram_cant = 100 #cantidad de ram disponible
procesos = 12 #cantidad de procesos a generar
work = 3 #cantidad de instrucciones por unidad de tiempo que trabaja el cpu
intervalo = 10.0 #intervalo en el que se enviaran las instrucciones


#variables que se van a usar durante el programa
#env = ambiente de simulacion
env = simpy.Environment()
#cpu = tipo resourse
cpu = simpy.Resource(env, capacity= cpu_cant)
#wait = seccion wait del sistema
wait = simpy.Resource(env, capacity=1)
#ram = tipo container
ram = simpy.Container(env, capacity= ram_cant, init= ram_cant)

#datos finales
tiempo_final = 0.0
desviacion_estandar = 0.0
promedio = 0.0
#se crean los procesos
for i in range(procesos):
    total_instrucciones = random.randint(1,10)
    total_ram = random.randint(1,10)
    delay = random.expovariate(1.0/intervalo)
    env.process(proceso('No.%s' %i, total_instrucciones, total_ram, delay, work))
#se inicia la simulacion
env.run()
#calculo del promedio
promedio = tiempo_final/procesos
#calculo de la desviacion estandar
desviacion_estandar = desviacion_estandar/procesos
desviacion_estandar = sqrt(desviacion_estandar)
print 'El tiempo total fue de: %s' %tiempo_final
print 'El promedio es de: %s' %promedio
print 'La desviacion estandar es de: %s' %desviacion_estandar