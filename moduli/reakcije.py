
# coding: utf-8

# # Preračun reakcij

# ## Reakcije

# In[1]:

import numpy as np


# In[2]:

from numpy.linalg import lstsq


# In[3]:

class Izracun:
    """
        return: seznam reakcij podpor A, B in C (če je samo A, so vse komponente B in C enake 0).
        """
    def __init__(self, oblika, vpetje, obremenitve):
        
        b = np.zeros((9,1))

        b[(0,0)] = -sum(j.vektor[0] for j in obremenitve)
        b[(1, 0)] = -sum(j.vektor[1] for j in obremenitve)
        b[(2, 0)] = -sum(j.vektor[2] for j in obremenitve)
        
        Ab = np.zeros((9,9))
        
        for i, j in enumerate(vpetje):
            Ab[(0, 3*i+0)] = j.vektor[(0,0)]
            Ab[(1, 3*i+1)] = j.vektor[(1,0)]
            Ab[(2, 3*i+2)] = j.vektor[(2,0)]
            Ab[(2, 3*i+1)] = j.lokacija
        
        self.resitve = lstsq(Ab, b)

