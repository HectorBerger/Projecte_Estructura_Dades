# -*- coding: utf-8 -*-
import json
import cfg
import platform
import sys
import os
import os.path
import uuid
from Gallery import Gallery
from ImageData import ImageData

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

from ImageData import ImageData

class SearchMetadata: 
    def __init__(self, image_data: ImageData = None):
        self._image_data = image_data or ImageData()

    def _search_field(self, field: str, sub: str) -> list:
        results = []
        for uuid, metadata in self._image_data:
            value = metadata.get(field)
            if value != None and value.find(sub) >= 0:
                results.append(uuid)
        return results

    def prompt(self, sub: str) -> list:
        return self._search_field('prompt', sub)
    
    def model(self, sub: str) -> list:
        return self._search_field('model', sub)
    
    def seed(self, sub: str) -> list:
        return self._search_field('seed', sub)
    
    def cfg_scale(self, sub: str) -> list:
        return self._search_field('cfg_scale', sub)

    def steps(self, sub: str) -> list:
        return self._search_field('steps', sub)
    
    def sampler(self, sub: str) -> list:
        return self._search_field('sampler', sub)
    
    def date(self, sub: str) -> list:
        # camp correcte a ImageData: 'created_date'
        return self._search_field('created_date', sub)
    
    def and_operator(self, list1: list, list2: list) -> list:
        return [x for x in list1 if x in list2]
    
    def or_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) | set(list2))
        
    def __str__(self):
        return 'SearchMetadata'
    
    def __len__(self):
        return 0
