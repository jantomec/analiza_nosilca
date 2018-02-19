
# coding: utf-8

# # Definiranje zunanjih obremenitev

# In[1]:

from scipy import integrate


# In[2]:

import numpy as np


# In[3]:

class Točkovna_sila:
    """Točkovna sila, kot - kot glede na x os v stopinjah."""
    def __init__(self, oblika, start, velikost, kot): #kot - kot glede na x os v stopinjah
        self.start = start
        self.velikost = velikost
        self.kot = kot
        self.stop = start
        self.obl = oblika
        self.tip = "Točkovna_sila"

        for i in self.obl:
            if i.startx <= self.start <= i.stopx:
                self.polozaj_y = i.mat_fun_obl(self.start)
    
        self.vektor = np.array([[self.velikost*np.cos(self.kot*np.pi/180)],    #x komponenta
                                [self.velikost*np.sin(self.kot*np.pi/180)],    #y komponenta
                                [self.velikost*np.sin(self.kot*np.pi/180)*self.start -
                                 self.velikost*np.cos(self.kot*np.pi/180)*self.polozaj_y]])   #moment okoli izhodišča
    
    def meje(self, X):
        """Definira, katere meje polj vključuje ta del.
        Input: X (rezultat funkcije polja.definiraj)
        self.moje_meje (seznam vključenih mej)"""
        
        moje_meje = []
        for i in X:
            if self.start <= i <= self.stop:
                moje_meje.append(i)
        return moje_meje


# In[4]:

class Kontinuirna_linearna:
    """Oblika v absolutnem koordinatnem sistemu: q(x) = kx + n. Smer je privzeto pravokotna na nosilec.
    Deluje samo na ravnem in vodoravnem nosilcu."""
    def __init__(self, oblika, start=0, stop=1, n=1, k=1):
        self.start = start
        self.stop = stop
        self.k = k
        self.n = n
        self.obl = oblika
        self.tip = "Kontinuirna_linearna"

        self.Q = lambda x: self.k*x + self.n
        self.Qx = lambda x: x*self.Q(x)
        
        self.velikost = -integrate.quad(self.Q, self.start, self.stop)[0]
        self.tezisce = -integrate.quad(self.Qx, self.start, self.stop)[0]/self.velikost
                
        self.vektor = np.array([[0],
                                [self.velikost],
                                [self.velikost*self.tezisce]])
    
    def meje(self, X):
        """Definira, katere meje polj vključuje ta del.
        Input: X (rezultat funkcije polja.definiraj)
        self.moje_meje (seznam vključenih mej)
        Return: /"""
        
        moje_meje = []
        for i in X:
            if self.start <= i <= self.stop:
                moje_meje.append(i)
        return moje_meje


# In[5]:

class Kontinuirna_kvadratna:
    """Oblika v absolutnem koordinatnem sistemu: q(x) = a0 + a1*x + a2*x**2.
    Smer je privzeto pravokotna na nosilec. Deluje samo na ravnem in vodoravnem nosilcu."""
    def __init__(self, oblika, start=0, stop=1, a0=0, a1=0, a2=1):
        self.start = start
        self.stop = stop
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.obl = oblika
        self.tip = "Kontinuirna_kvadratna"

        self.Q = lambda x: self.a0 + self.a1*x + self.a2*x**2
        self.Qx = lambda x: x*self.Q(x)
        self.velikost = -integrate.quad(self.Q, self.start, self.stop)[0]
        self.tezisce = -integrate.quad(self.Qx, self.start, self.stop)[0]/self.velikost
                
        self.vektor = np.array([[0],
                                [self.velikost],
                                [self.velikost*self.tezisce]])
    
    def meje(self, X):
        """Definira, katere meje polj vključuje ta del.
        Input: X (rezultat funkcije polja.definiraj)
        self.moje_meje (seznam vključenih mej)
        Return: /"""
        
        moje_meje = []
        for i in X:
            if self.start <= i <= self.stop:
                moje_meje.append(i)
        return moje_meje


# In[6]:

class Moment:
    """smer (1 ali -1) - smer vrtenja"""
    def __init__(self, oblika, start=0, velikost=1, smer=1): #smer (1 ali -1) - smer vrtenja
        self.start = start
        self.velikost = velikost
        self.smer = smer
        self.stop = start
        self.obl = oblika
        self.tip = "Moment"

        for i in self.obl:
            if i.startx <= self.start <= i.stopx:
                self.polozaj_y = i.mat_fun_obl(self.start)
        self.vektor = np.zeros((3, 1))
        self.vektor[2] = self.velikost*self.smer
    
    def meje(self, X):
        """Definira, katere meje polj vključuje ta del.
        Input: X (rezultat funkcije polja.definiraj)
        self.moje_meje (seznam vključenih mej)
        Return: /"""
        
        moje_meje = []
        for i in X:
            if self.start <= i <= self.stop:
                moje_meje.append(i)
        return moje_meje


# In[7]:

class User_defined:
    """Katerakoli numpy funkcija oblike y = f(x)."""
    def __init__(self, fun_x, fun_y, start, stop):
        self.fun = fun
        self.start = start
        self.stop = stop
        self.velikost_x = integrate.quad(fun_x, start, stop)[0]
        self.velikost_y = integrate.quad(fun_y, start, stop)[0]
        fun_xx = lambda x: fun_x(x)*x
        def fun_yy(x):
            for i in oblika:
                if i.startx <= x <= i.stopx:
                    y = i.mat_fun_obl(x)
            return fun_y(x)*y
        tezisce_x = integrate.quad(fun_xx, start, stop)[0]/self.velikost
        tezisce_y = integrate.quad(fun_yy, start, stop)[0]/self.velikost
        self.tezisce_x = tezisce_x[0]
        self.tezisce_y = tezisce_y[0]
        


# In[ ]:



