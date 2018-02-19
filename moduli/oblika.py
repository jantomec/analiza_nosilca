
# coding: utf-8

# # Matematična definicija oblike

# Uporabljal bom knjižnico numpy.

# In[1]:

import numpy as np


# Zdefinirani sta zaenkrat dve obliki nosilca, in sicer raven nosilec in nosilec v obliki krožnega loka.
# 
# Vsaka oblika ima svoj razred, zato, da je čim preprostejše vnašanje vhodnih podatkov za nosilec.

# In[2]:

class Raven:
    """Razred za ravno obliko nosilca."""
    def __init__(self, start=[0, 0], stop=[1, 1]):
        self.startx = start[0]
        self.starty = start[1]
        self.stopx = stop[0]
        self.stopy = stop[1]
        self.kot = np.arctan((self.stopy - self.starty)/(self.stopx - self.startx))
    
    
    def mat_fun_obl(self, x): #matematična funkcija oblike
        try:
            return (self.stopy - self.starty)/(self.stopx - self.startx)*(x - self.stopx) + self.stopy
        except ZeroDivisionError:
            print("Navpičen nosilec.")

    
    def meje(self, X):
        """Definira, katere meje polj vključuje ta del.
        Input: X (rezultat funkcije polja.definiraj)
        self.moje_meje (seznam vključenih mej)
        """
        
        moje_meje = []
        for i in X:
            if self.startx <= i <= self.stopx:
                moje_meje.append(i)
        return moje_meje


# In[3]:

class Arc:
    """Razred za nosilec oblike krožnega loka."""
    def __init__(self, start=[0, 0], center=[0, 1], kot=90, a_predznak=1): #kot v stopinjah
        self.startx = start[0]
        self.starty = start[1]
        self.centerx = center[0]
        self.centery = center[1]
        self.kot = kot
        self.R = np.sqrt((self.centerx - self.startx)**2 + (self.centery - self.starty)**2)
        self.stopx = self.startx + np.sin(kot*np.pi/180)*self.R
        self.a_predznak = a_predznak

    
    def mat_fun_obl(self, x): #matematična funkcija oblike
        try:
            a = (self.centery - self.starty)/abs(self.centery - self.starty) #+/- 1, gelde na to, kateri del krožnice opazujemo
        except ZeroDivisionError:
            a = -self.a_predznak
        return self.centery - a*np.sqrt(self.R**2 - (x - self.centerx)**2)

    
    def meje(self, X):
        """Definira, katere meje polj vključuje ta del.
        Input: X (rezultat funkcije polja.definiraj)
        self.moje_meje (seznam vključenih mej)
        Return: /"""
        
        moje_meje = []
        for i in X:
            if self.startx <= i <= self.stopx:
                moje_meje.append(i)
        return moje_meje


# In[ ]:



