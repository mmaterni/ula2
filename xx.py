#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# def handle_duplicates(lst):
#     n = {x: 0 for x in set(lst)}
#     row = []
#     for x in lst:
#         n[x] += 1
#         row.append(f"{x}.{n[x]}")
#     return row

# my_list = ['a', 'b', 'c', 'a', 'b', 'a']
# result_list = handle_duplicates(my_list)
# print(result_list)

# def handle_duplicates(lst):
#     counts = {}
#     return list(
#         map(
#             lambda x: f"{x}.{counts.setdefault(x, 0) + 1}"
#             if x in counts else x, lst))

# my_list = ['a', 'b', 'c', 'a', 'b', 'a']
# result_list = handle_duplicates(my_list)
# print(result_list)

# def handle_duplicates(lst):
#     n = {}
#     return [
#         f"{x}.{n.setdefault(x, 0) + 1}" if (n[x] := n.get(x)) else
#         (n.update({x: 1}), x) for x in lst
#     ]

# # Esempio di utilizzo
# my_list = ['a', 'b', 'c', 'a', 'b', 'a']
# result_list = handle_duplicates(my_list)
# print(result_list)
# def rimuovi_duplicati(lista):
#     lista_senza_duplicati = []
#     [lista_senza_duplicati.append(elemento) for elemento in lista if elemento not in lista_senza_duplicati]
#     return lista_senza_duplicati

# lista_input = ['a', 'a', 'a', 'b', 'c', 'c', 'c']
# lista_output = rimuovi_duplicati(lista_input)
# print(lista_output)

# def rimuovi_duplicati(lista):
#     return [elemento for elemento in lista if lista.count(elemento) == 1]

# lista_input = ['a', 'a', 'a', 'b', 'c', 'c', 'c']
# lista_output = rimuovi_duplicati(lista_input)
# print(lista_output)

from collections import OrderedDict

def rimuovi_duplicati(lista):
    # print(OrderedDict.fromkeys(lista))
    # lst=[x for x in OrderedDict.fromkeys(lista,'')]
    # return lst
    return list(OrderedDict.fromkeys(lista))

lista_input = ['x','b', 'b', 'b', 'a', 'c', 'c', 'c']
lista_output = rimuovi_duplicati(lista_input)
print(lista_output)

