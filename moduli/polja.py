
# coding: utf-8

# # Definiranje polj

# In[1]:

def definiraj(oblika, vpetje, obremenitve): #oblika, vpetje in obremenitve moraj biti v obliki seznama
    X = set()

    for i in oblika:
        X.add(i.startx)
        if hasattr(i, "stopx"):
            X.add(i.stopx)
        else:
            X.add(i.centerx)
            X.add(i.stop)

    for i in vpetje:
        X.add(i.lokacija)

    for i in obremenitve:
        if hasattr(i, "start"):
            X.add(i.start)
            X.add(i.stop)
        else:
            X.add(i.lokacija)
    
    X = list(X)
    x = X.sort()
    return X


# In[2]:

class i_polje:
    """
    Definicija posameznega polja.
    parameter n - zaporedna številka polja
    x_spodnji - spodnja meja predstavlja začetek polja
    x_zgornji - zgornja meja predstavlja konec polja
    tip - glede na potek strižnih sil v polju [konstantni, linearni, kvadratni]
    """
    def __init__(self, n, x_spodnji, x_zgornji):

        self.spodnja_meja = x_spodnji #spodnja meja predstavlja začetek polja
        self.zgornja_meja = x_zgornji
        
        def int_to_roman(input_rom):                # Konverter v rimske številke. Nisem avtor te funkcije.
            """ Convert an integer to a Roman numeral. """
            ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
            nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
            result = []
            for i in range(len(ints)):
                count = int(input_rom / ints[i])
                result.append(nums[i] * count)
                input_rom -= ints[i] * count
            return ''.join(result)
        
        self.ime = "{i}. polje".format(i=int_to_roman(n))
        

