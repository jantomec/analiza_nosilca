
# coding: utf-8

# # Iskanje ničel osne in strižna sila ter momenta

# Ker kalkulator ne uporablja enotne funkcije za računanje nosilca, temveč to dela po poljih, nisem uporabil scipy vgrajenih funkcij za iskanje ničel, temveč sem spisal kodo, ki je prilagojena kalkulatorju in izkorišča že izračunane podatke

# In[1]:

import numpy as np


# In[3]:

class iskanje:
    def __init__(self, notomox):
        """Pri čemer obj predstavlja objekt, ki ga ustvarimo z modulom izris."""
        self.seznam = notomox

        self.Nmax = []
        self.N_vrednosti_max = []
        self.Tmax = []
        self.T_vrednosti_max = []
        self.Mmax = []
        self.M_vrednosti_max = []

        winner_n = np.argwhere(np.abs(self.seznam[1]) == np.amax(np.abs(self.seznam[1]))).flatten()
        self.N_vrednost = np.amax(np.abs(self.seznam[1]))
        for n in winner_n:
            self.Nmax.append(self.seznam[0, n])
        winner_t = np.argwhere(np.abs(self.seznam[2]) == np.amax(np.abs(self.seznam[2]))).flatten()
        self.T_vrednost = np.amax(np.abs(self.seznam[2]))
        for t in winner_t:
            self.Tmax.append(self.seznam[0, t])
        winner_m = np.argwhere(np.abs(self.seznam[3]) == np.amax(np.abs(self.seznam[3]))).flatten()
        self.M_vrednost = np.amax(np.abs(self.seznam[3]))
        for m in winner_m:
            self.Mmax.append(self.seznam[0, m])

        for x in self.Nmax:
            for i, j in enumerate(self.seznam[0]):
                if x == j:
                    self.N_vrednosti_max.append(self.seznam[(1, i)])
                    break

        for x in self.Tmax:
            for i, j in enumerate(self.seznam[0]):
                if x == j:
                    self.T_vrednosti_max.append(self.seznam[(2, i)])
                    break

        for x in self.Mmax:
            for i, j in enumerate(self.seznam[0]):
                if x == j:
                    self.M_vrednosti_max.append(self.seznam[(3, i)])
                    break


# In[ ]:



