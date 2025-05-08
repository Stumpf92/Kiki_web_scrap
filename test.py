#'informationsgewinn'

import math

data_before = [
    'blau', 'rot', 'rot', 'rot', 'rot', 'rot']
data_after = [
    'blau', 'rot', 'rot', 'rot', 'rot']

def get_entropie(data):
    length = len(data)
    menge_an_ereignissen = set(data)
    paar_ereigniss_häufigkeit = []
    for i in menge_an_ereignissen:
        paar_ereigniss_häufigkeit.append([i, data.count(i)])
    
    entropie = 0
    for i in paar_ereigniss_häufigkeit:
        p_i = i[1]/length
        entropie_i = p_i * math.log2(1/p_i)
        entropie += entropie_i
    print(entropie)
    return entropie
        
ig = get_entropie(data_before) - get_entropie(data_after)
print(ig)