
# coding: utf-8

# # Podajanje vpetja

# In[1]:

import numpy as np


# In[1]:

class Konzola:
    """Konzola - preprečuje translacijo in rotacijo.
    Lokacija - koordinata x v absolutnem koordinatnem sistemu."""
    def __init__(self, oblika, lokacija): #lokacija - koordinata x v absolutnem koordinatnem sistemu
        self.lokacija = lokacija
        self.vektor = np.ones((3,1))
        self.kot = 0
        
        for i in oblika:
            if i.startx <= self.lokacija <= i.stopx:
                self.polozaj_y = i.mat_fun_obl(self.lokacija)
    
    def reakcije_v_podporah(self, A_reakcije):
        """Spremeni vektor reakcij iz splošnega v izračunanega."""
        self.vektor_reakcij = A_reakcije


# In[2]:

class Nepomična_podpora:
    """Konzola - preprečuje translacijo ne pa tudi rotacije.
    Lokacija - koordinata x v absolutnem koordinatnem sistemu."""
    def __init__(self, oblika, lokacija):
        self.lokacija = lokacija
        self.vektor = np.ones((3,1))
        self.vektor[(2,0)] = 0
        self.kot = 0
        
        for i in oblika:
            if i.startx <= self.lokacija <= i.stopx:
                self.polozaj_y = i.mat_fun_obl(self.lokacija)
        
    def reakcije_v_podporah(self, A_reakcije):
        """Spremeni vektor reakcij iz splošnega v izračunanega."""
        self.vektor_reakcij = A_reakcije


# In[3]:

class Pomična_podpora:
    """Konzola - preprečuje translacijo v eni smeri ne pa tudi rotacije.
    Lokacija - koordinata x v absolutnem koordinatnem sistemu.
    Kot glede na x os v stopinjah za os, v kateri translacija ni preprečena."""
    def __init__(self, oblika, lokacija, kot=0): #os - kot glede na x os v stopinjah za os, v kateri translacija ni preprečena.
        self.lokacija = lokacija
        self.kot = kot
        self.vektor = np.zeros((3,1))
        self.vektor[(0,0)] = -np.sin(self.kot*np.pi/180)
        self.vektor[(1,0)] = np.cos(self.kot*np.pi/180)
        self.vektor[(2,0)] = 0
        
        for i in oblika:
            if i.startx <= self.lokacija <= i.stopx:
                self.polozaj_y = i.mat_fun_obl(self.lokacija)

    def reakcije_v_podporah(self, A_reakcije):
        """Spremeni vektor reakcij iz splošnega v izračunanega."""
        self.vektor_reakcij = A_reakcije


# In[ ]:



