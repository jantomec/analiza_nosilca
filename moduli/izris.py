
# coding: utf-8

# # Izris NTM diagramov

# In[1]:

from moduli import polja, modul_notranje_sile

# In[3]:

from sympy import *


# In[4]:

import numpy as np


# In[5]:

import matplotlib.pyplot as plt
import matplotlib as mpl

from moduli import modul_nicle

# In[6]:

get_ipython().magic('matplotlib inline')


# In[7]:

class NTM:
    def __init__(self, oblika, obremenitve, vpetje, notranje_sile):
        self.obl = oblika
        self.obrm = obremenitve
        self.vpet = vpetje
        self.notr_sile = notranje_sile
        self.xos = []
        #self.Nos = self.notranje_sile.NTM[0]
        #self.Tos = self.notranje_sile.NTM[1]
        #self.Mos = self.notranje_sile.NTM[2]
        self.mat_obl = []

        dx = 1/1000

        for i, x in enumerate(self.notr_sile.numb):
            if i == 0:
                self.xos.append(x)
                self.xos.append(x+dx)
            else:
                self.xos.append(x-dx)
                self.xos.append(x)

        self.notomox = np.vstack((self.xos, self.notr_sile.NTM))

        for i in self.obrm:
            if i.tip in ["Kontinuirna_linearna", "Kontinuirna_kvadratna"]:
                po = []
                for p in self.notr_sile.numb:
                    if i.start <= p <= i.stop:
                        po.append(p)
                for n in range(len(po)-1):
                    i_xos = np.linspace(po[n], po[n+1], 1000)
                    i_ntm = modul_notranje_sile.NTM_lin_quad(self.obl, self.obrm, self.vpet, u_numb=i_xos).NTM_lin_quad
                    self.notomox = np.concatenate((self.notomox, i_ntm), axis=1)

        for j in self.obl:
            if hasattr(j, "centerx"):
                po = []
                for p in self.notr_sile.numb:
                    if j.startx <= p <= j.stopx:
                        po.append(p)
                for n in range(len(po)-1):
                    i_xos = np.linspace(po[n], po[n+1], 1000)
                    i_ntm = modul_notranje_sile.NTM_lin_quad(self.obl, self.obrm, self.vpet, u_numb=i_xos).NTM_lin_quad
                    self.notomox = np.concatenate((self.notomox, i_ntm), axis=1)
    

        self.notomox = self.notomox[:, np.argsort(self.notomox[0,:])] #ureditev stolpcev glede na prvo vrstico (x)
        self.xos = self.notomox[0]
        self.Nos = self.notomox[1]
        self.Tos = self.notomox[2]
        self.Mos = self.notomox[3]
        
        for x in self.xos:
            for i in self.obl:
                if i.startx <= x <= i.stopx:
                    self.mat_obl.append(i.mat_fun_obl(x))
                    break
        
        self.najvec = max([max(self.Nos), max(self.Tos), max(self.Mos), max(self.mat_obl)])
        self.najmanj = min([min(self.Nos), min(self.Tos), min(self.Mos), max(self.mat_obl)])

        if self.najmanj < 0:
            self.najmanj = 1.2*self.najmanj
        else:
            self.najmanj = 0
        if self.najvec > 0:
            self.najvec = 1.2*self.najvec
        else:
            self.najvec = 0

    def izris(self, shrani=False, ekstremi=False):
        self.nicle = modul_nicle.iskanje(self.notomox)
        
        f, (skica, axN, axT, axM) = plt.subplots(4, sharex=False, sharey=True, squeeze=True, figsize=(7,15))
        skica.plot(self.xos, self.mat_obl, 'k', linewidth=5)
        skica.set_ylabel("y", fontsize = 14)
        skica.spines['bottom'].set_position('zero')
        skica.spines['top'].set_color('none')
        skica.spines['left'].set_smart_bounds(False)
        skica.spines['bottom'].set_smart_bounds(True)
        skica.yaxis.set_ticks_position('left')
        skica.xaxis.set_ticks_position('bottom')
        
        axN.plot(self.xos, self.Nos)
        axN.set_ylabel("N", fontsize = 15)
        axN.set_xlabel("x", fontsize = 15, x=1.05)
        axN.xaxis.set_label_coords(1.05, 0)
        axN.set_xlim(min(self.xos), max(self.xos))
        axN.set_ylim([self.najmanj, self.najvec])
        axN.spines['bottom'].set_position('zero')
        axN.spines['top'].set_color('none')
        axN.spines['left'].set_smart_bounds(False)
        axN.spines['bottom'].set_smart_bounds(True)
        axN.xaxis.set_ticks_position('bottom')
        axN.yaxis.set_ticks_position('left')
        axN.fill_between(self.xos, 0, self.Nos, hatch='/', edgecolor='blue', facecolor='none', linewidth='3')
        if ekstremi:
            axN.plot(self.nicle.Nmax, self.nicle.N_vrednosti_max, 'o', markersize=10)

        axT.plot(self.xos, self.Tos)
        axT.set_ylabel("T", fontsize = 15)
        axT.set_xlabel("x", fontsize = 15, x=1.05)
        axT.xaxis.set_label_coords(1.05, 0)
        #axT.set_xlim(min(self.xos), max(self.xos))
        axT.spines['bottom'].set_position('zero')
        axT.spines['top'].set_color('none')
        axT.spines['left'].set_smart_bounds(False)
        axT.spines['bottom'].set_smart_bounds(True)
        axT.xaxis.set_ticks_position('bottom')
        axT.yaxis.set_ticks_position('left')
        axT.fill_between(self.xos, 0, self.Tos, hatch='/', edgecolor='blue', facecolor='none', linewidth='3')
        if ekstremi:
            axT.plot(self.nicle.Tmax, self.nicle.T_vrednosti_max, 'o', markersize=10)

        axM.plot(self.xos, self.Mos)
        axM.set_ylabel("M", fontsize = 15)
        axM.set_xlabel("x", fontsize = 15, x=1.05)
        axM.xaxis.set_label_coords(1.05, 0)
        axM.spines['bottom'].set_position('zero')
        axM.spines['top'].set_color('none')
        axM.spines['left'].set_smart_bounds(False)
        axM.spines['bottom'].set_smart_bounds(True)
        axM.xaxis.set_ticks_position('bottom')
        axM.yaxis.set_ticks_position('left')
        axM.fill_between(self.xos, 0, self.Mos, hatch='/', edgecolor='blue', facecolor='none', linewidth='3')
        if ekstremi:
            axM.plot(self.nicle.Mmax, self.nicle.M_vrednosti_max, 'o', markersize=10)

        f.subplots_adjust(hspace=0)
        
        if shrani:
            plt.savefig("diagrami.png")

