
def l1l2(lista_1, lista_2):
    # risultato = [x if x in lista_2 else '' for x in lista_1]
    rs = [() for x in lista_1]
    return rs


l1 = ['pippo', 'lillo', 'pluto', 'fido', 'argo', 'cesare']
l2 = ['cesare', 'fido', 'lillo']

l=l1l2(l1,l2)
print(l)