from constantes import *
import numpy as np
import matplotlib.pyplot as plt 
from math import *
from scipy.integrate import odeint
rpm = np.arange(1000,8001,1)

def torquegeral(w):
    if 1000<=w<=1500:
        return 0.18*w - 60
    elif 1500<w<=2000:
        return 0.05*w + 135
    elif 2000<w<=3000:
        return -0.045*w + 325
    elif 3000<w<=3500:
        return -0.03*w + 280
    elif 3500<w<=4000:
        return -0.05*w + 350
    elif 4000<w<=4500:
        return -0.04*w + 310
    elif 4500<w<=8000:
        return -0.06*w + 400
def torque(w,rtrans):
    torqueg = torquegeral(w)
    return torqueg*rtrans
 
def angular(w, rtrans):
    return w / rtrans

t1 = []
t2 = []
t3 = []
t4 = []
w1 = []
w2 = []
w3 = []
w4 = []

for i in rpm:
    t1.append(torque(i,n["1"]))
    t2.append(torque(i,n["2"]))
    t3.append(torque(i,n["3"]))
    t4.append(torque(i,n["4"]))
    w1.append(angular(i,n["1"]))
    w2.append(angular(i,n["2"]))
    w3.append(angular(i,n["3"]))
    w4.append(angular(i,n["4"]))

plt.plot(w1, t1, label = "1a marcha")
plt.plot(w2, t2, label = "2a marcha")
plt.plot(w3, t3, label = "3a marcha")
plt.plot(w4, t4, label = "4a marcha")
plt.legend()
plt.grid()

rpm_lista = np.arange(61,4000,1)
torque_lista = [0]*len(rpm_lista)

for i in range(0,len(rpm_lista)):
    for j in range(0,len(w1)):
        if w1[j] > rpm_lista[i]:
            torque_lista[i] = t1[j]
            break
    for j in range(0,len(w2)):
        if w2[j] > rpm_lista[i]:
            torque_lista[i] = max(torque_lista[i],t2[j])
            break 
    for j in range(0,len(w3)):
        if w3[j] > rpm_lista[i]:
            torque_lista[i] = max(torque_lista[i],t3[j])
            break 
    for j in range(0,len(w4)):
        if w4[j] > rpm_lista[i]:
            torque_lista[i] = max(torque_lista[i],t4[j])
            break 
valorinicial = torque_lista[0]
lista = [valorinicial]*61
torque_lista = lista + torque_lista
           
lrpm = np.arange(0,4000,1)
rpm_lista = lrpm

plt.plot(rpm_lista,torque_lista,'r--')
plt.show()

def modelo(z,t):
    s = z[0]
    v = z[1]
    if 0<=v<6.98:
        valor = "1"
    elif 6.98<=v<12.6:
        valor="2"
    elif 12.6<=v<19:
        valor = '3'    
    elif 19<v:
        valor = "4"      
    w = v/r 
    rpm = w *30 / pi
    rpm = int(rpm)
    for i in range(len(rpm_lista)):
        if rpm == rpm_lista[i]:
            tq = torque_lista[i]
            break        
    T = tq/r
    D = 0.5 * p*A*Cw*v**2
    dsdt = v
    dvdt = (T-D)/m
    return [dsdt,dvdt]

s0 = 0
v0 = 0
z0 = [s0,v0]

dt = 1e-3
listat = np.arange(0,20,dt)

z = odeint(modelo, z0, listat)
s = z[:,0]
v = z[:,1]

# plt.plot(listat, s)
# plt.grid()
# plt.show()

plt.plot(listat, v*3.6)
plt.grid()
plt.show()