
# coding: utf-8

# # Preračun notranjih sil in momentov

# In[1]:

import numpy as np


# In[2]:

from numpy.linalg import solve


# In[3]:

from scipy import integrate


# In[4]:

from moduli import polja, reakcije


# In[6]:

from scipy.misc import derivative


# In[7]:

class NTM:
    """Izračun NTM po poljih. Parametri: oblika, vpetje, obremenitve, reakcije"""
    def __init__(self, oblika, obremenitve, vpetje):

        self.numb = polja.definiraj(oblika, vpetje, obremenitve)
        
        self.obl = oblika
        self.obrm = obremenitve
        self.vpet = vpetje
        self.reakc = reakcije.Izracun(self.obl, self.vpet, self.obrm).resitve[0]
        
        for i, j in enumerate(self.vpet):
            j.reakcije_v_podporah(np.split(self.reakc, 3, axis=0)[i])
        
        def NTM_izracun(matrika_A, vektor_b):
            """
            x, y - sta koordinati točke x_i v kateri računamo NTM.
            α - kot tangente glede na obliko v točki
            b - vektor obremenitev v polju med točkama x_i-1 in x_i
            v - vektor NTM sil v točki x_i-1
            """
            
            ntm = solve(matrika_A, vektor_b)
            return ntm
        
        self.NTM = np.zeros((3,1))
        b0 = np.zeros((3,1)) #v točki x - dx
        b1 = b0              #b1 je v točki x
        
        for i, x in enumerate(self.numb):

            α = [] #pri enem x sta kvečjemu dva kota, ne nujno enaka (lomljeni nosilec)
            for j in self.obl:
                _meje = j.meje(self.numb)
                if x in _meje:
                    y = j.mat_fun_obl(x)
                    d_x = 1/1000
                    if x == j.startx:
                        delta_y = j.mat_fun_obl(x + d_x) - y
                    else:
                        delta_y = y - j.mat_fun_obl(x - d_x)
                    α.append(np.arctan2(delta_y, d_x))
            if len(α) == 1:
                α.append(α[0])
            if i == 0:
                A1 = np.array([[np.cos(α[0]), np.cos(α[0] + np.pi/2), 0], #tak zapis zaradi predznakov
                               [np.sin(α[0]), np.sin(α[0] + np.pi/2), 0],
                               [(y*np.cos(α[0]) + x*np.sin(α[0])), (y*np.cos(α[0] + np.pi/2) + x*np.sin(α[0] + np.pi/2)), 1]])
            elif i == len(self.numb):
                A0 = np.array([[np.cos(α[0]), np.cos(α[0] + np.pi/2), 0],
                               [np.sin(α[0]), np.sin(α[0] + np.pi/2), 0],
                               [(y*np.cos(α[0]) + x*np.sin(α[0])), (y*np.cos(α[0] + np.pi/2) + x*np.sin(α[0] + np.pi/2)), 1]])
            else:
                A0 = np.array([[np.cos(α[0]), np.cos(α[0] + np.pi/2), 0],
                               [np.sin(α[0]), np.sin(α[0] + np.pi/2), 0],
                               [(y*np.cos(α[0]) + x*np.sin(α[0])), (y*np.cos(α[0] + np.pi/2) + x*np.sin(α[0] + np.pi/2)), 1]])
                A1 = np.array([[np.cos(α[1]), np.cos(α[1] + np.pi/2), 0],
                               [np.sin(α[1]), np.sin(α[1] + np.pi/2), 0],
                               [(y*np.cos(α[1]) + x*np.sin(α[1])), (y*np.cos(α[1] + np.pi/2) + x*np.sin(α[1] + np.pi/2)), 1]])
            
            b0 = b1
            if i > 0: #določim b0
                for j in self.obrm:
                    _meje = j.meje(self.numb)
                    if self.numb[i-1] in _meje[:-1]:
                        #if j.tip == "Točkovna_sila":
                            #b0 = b0 - j.vektor
                        if j.tip == "Kontinuirna_linearna":
                            vekt = np.zeros((3,1))
                            velikost = -integrate.quad(j.Q, self.numb[i-1], x)[0]
                            vekt[(1,0)] = velikost
                            xt = -integrate.quad(j.Qx, self.numb[i-1], x)[0]/velikost
                            vekt[(2,0)] = xt*velikost
                            b0 = b0 - vekt
                        elif j.tip == "Kontinuirna_kvadratna":
                            vekt = np.zeros((3,1))
                            velikost = -integrate.quad(j.Q, self.numb[i-1], x)[0]
                            vekt[(1,0)] = velikost
                            xt = -integrate.quad(j.Qx, self.numb[i-1], x)[0]/velikost
                            vekt[(2,0)] = xt*velikost
                            b0 = b0 - vekt
                        #elif j.tip == "Moment":
                            #b0 = b0 - j.vektor
            
            b1 = b0
            for j in self.obrm: #določim b1
                _meje = j.meje(self.numb)
                if x in _meje:
                    if j.tip == "Točkovna_sila":
                        b1 = b1 - j.vektor
                    #elif j.tip == "Kontinuirna_linearna":
                        #b1 = b0
                    #elif j.tip == "Kontinuirna_kvadratna":
                        #b1 = b0
                    elif j.tip == "Moment":
                        b1 = b1 - j.vektor
            for j in self.vpet:
                if x == j.lokacija:
                    vekt = j.vektor_reakcij
                    vekt[(2,0)] = vekt[(2,0)] + j.lokacija*vekt[(1,0)]
                    b1 = b1 - vekt
            
            if i > 0:
                i_ntm0 = NTM_izracun(A0, b0)
                self.NTM = np.column_stack((self.NTM, i_ntm0))
            i_ntm1 = NTM_izracun(A1, b1)
            self.NTM = np.column_stack((self.NTM, i_ntm1))


# In[8]:

class NTM_lin_quad:
    """Izračun NTM po točkah (delčkih nosilca). Parametri: oblika, vpetje, obremenitve, reakcije, seznam točk.
       Izračun poteka samo znotraj enega polja."""
    def __init__(self, oblika, obremenitve, vpetje, u_numb=["seznam točk za izračun"]):

        self.numb = u_numb
        self.obl = oblika
        self.obrm = obremenitve
        self.vpet = vpetje
        self.reakc = reakcije.Izracun(self.obl, self.vpet, self.obrm)
        
        def NTM_lin_quad_izracun(matrika_A, vektor_b):
            ntm = solve(matrika_A, vektor_b)
            return ntm
        
        #self.NTM_lin_quad = np.zeros((3,1))
        #b0 = np.zeros((3,1)) #v točki x
        
        self.start = self.numb[0]
        self.stop = self.numb[-1]
        
        b_zun = np.zeros((3,1)) #obremenitve pred začetkom polja, enak pomen kot b0, vendar različno fizikalno ozadje
        
        for i in vpetje:
            if i.lokacija <= self.start:
                vekt = i.vektor_reakcij
                vekt[(2,0)] = vekt[(2,0)] + i.lokacija*vekt[(1,0)]
                b_zun = b_zun + vekt
        
        for i in obremenitve:
            if i.tip in ["Točkovna_sila", "Moment"]:
                if i.start <= self.start:
                    b_zun = b_zun + i.vektor
            else:
                if i.tip in ["Kontinuirna_linearna", "Kontinuirna_kvadratna"]:
                    if i.start < self.start:
                        if i.stop <= self.start:
                            b_zun = b_zun + i.vektor
                        else:
                            vekt = np.zeros((3,1))
                            velikost = -integrate.quad(i.Q, i.start, self.start)[0]
                            vekt[(1,0)] = velikost
                            xt = -integrate.quad(i.Qx, i.start, self.start)[0]/velikost
                            vekt[(2,0)] = xt*velikost
                            b_zun = b_zun + vekt
        
        for i, x in enumerate(self.numb):

            α = []
            for j in self.obl:
                _meje = j.meje(self.numb)
                if x in _meje:
                    y = j.mat_fun_obl(x)
                    d_x = 1/10000
                    if x == j.startx:
                        delta_y = j.mat_fun_obl(x + d_x) - y
                    else:
                        delta_y = y - j.mat_fun_obl(x - d_x)
                    α.append(np.arctan2(delta_y, d_x))
            
            A0 = np.array([[np.cos(α[0]), np.cos(α[0] + np.pi/2), 0], #tak zapis zaradi predznakov
                           [np.sin(α[0]), np.sin(α[0] + np.pi/2), 0],
                           [(y*np.cos(α[0]) + x*np.sin(α[0])), (y*np.cos(α[0] + np.pi/2) + x*np.sin(α[0] + np.pi/2)), 1]])
            if i == 0:
                b0 = -b_zun
                i_ntm0 = NTM_lin_quad_izracun(A0, b0)
                self.NTM_lin_quad = i_ntm0
                
            else:
                for k in self.obrm:
                    if k.tip in ["Kontinuirna_linearna", "Kontinuirna_kvadratna"]:
                        if k.stop > self.start:
                            vekt = np.zeros((3,1))
                            velikost = -integrate.quad(k.Q, self.start, x)[0]
                            vekt[(1,0)] = velikost
                            xt = -integrate.quad(k.Qx, self.start, x)[0]/velikost
                            vekt[(2,0)] = xt*velikost
                            b0 = -(b_zun + vekt)
                
                i_ntm0 = NTM_lin_quad_izracun(A0, b0)
                self.NTM_lin_quad = np.column_stack((self.NTM_lin_quad, i_ntm0))
        
        self.NTM_lin_quad = np.vstack((self.numb, self.NTM_lin_quad))

