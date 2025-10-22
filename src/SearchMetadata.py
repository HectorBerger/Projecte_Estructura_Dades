# -*- coding: utf-8 -*-
import json
import ImageData 
import cfg
import platform
import sys
import os
import os.path
import uuid
from Gallery import Gallery
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""

class SearchMetadata (): 
    def __init__ (self):
        pass

    def prompt (self, sub: str):
        values  = []
        for uuid, metadata in self._hash:
            if metadata['prompt'].find(sub) != -1:
                values.append(uuid)
        return Gallery(values, 'prompt', sub)
    
    def model (self, sub: str):
        values  = []
        for uuid, metadata in self._hash:
            if metadata['model'].find(sub) != -1:
                values.append(uuid)
        return Gallery(values, 'model', sub)
    
    def seed (self, sub: str):
        values  = []
        for uuid, metadata in self._hash:
            if metadata['seed'].find(sub) != -1:
                values.append(uuid)

        return Gallery(values, 'seed', sub)
    
    def cfg_scale (self, sub: str):
        values  = []
        for uuid, metadata in self._hash:
            if metadata['cfg_scale'].find(sub) != -1:
                values.append(uuid)
        return Gallery(values, 'cfg_scale', sub)

    def steps (self, sub: str):
        values  = []
        for uuid, metadata in self._hash:
            if metadata['steps'].find(sub) != -1:
                values.append(uuid)
        return Gallery(values, 'steps', sub)
    
    def sampler (self, sub: str):
        values  = []
        for uuid, metadata in self._hash:
            if metadata['sampler'].find(sub) != -1:
                values.append(uuid)
        return Gallery(values, 'sampler', sub)
    
    def date (self, sub:str):
        values  = []
        for uuid, metadata in self._hash:
            if metadata['date'].find(sub) != -1:
                values.append(uuid)
        return Gallery(values, 'date', sub)
    
    def and_operator (self, list1: list, list2: list):
        return [x for x in list1 if x in list2]
    
    def or_opperator (self, list1: list, list2: list):
        return list( set(list1) | set(list2))

        
